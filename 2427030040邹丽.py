import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import date, datetime
import os  # 用于文件操作

# ====================== 全局页面配置 ======================
st.set_page_config(page_title="全维度数字生活管理系统", layout="wide")

# ====================== 默认模拟数据（仅首次启动使用） ======================
init_social = pd.DataFrame([
    {"日期":"2026-08-26","周期":"上周","APP":"微信","时长":2.0},
    {"日期":"2026-08-27","周期":"上周","APP":"微信","时长":2.2},
    {"日期":"2026-08-28","周期":"上周","APP":"微信","时长":1.8},
    {"日期":"2026-08-29","周期":"上周","APP":"微信","时长":2.5},
    {"日期":"2026-08-30","周期":"上周","APP":"微信","时长":2.1},
    {"日期":"2026-08-26","周期":"上周","APP":"抖音","时长":1.5},
    {"日期":"2026-08-27","周期":"上周","APP":"抖音","时长":1.7},
    {"日期":"2026-08-28","周期":"上周","APP":"抖音","时长":1.3},
    {"日期":"2026-08-29","周期":"上周","APP":"抖音","时长":2.0},
    {"日期":"2026-08-30","周期":"上周","APP":"抖音","时长":1.6},
    {"日期":"2026-09-02","周期":"本周","APP":"微信","时长":1.6},
    {"日期":"2026-09-03","周期":"本周","APP":"微信","时长":1.5},
    {"日期":"2026-09-04","周期":"本周","APP":"微信","时长":1.4},
    {"日期":"2026-09-05","周期":"本周","APP":"微信","时长":1.7},
    {"日期":"2026-09-06","周期":"本周","APP":"微信","时长":1.3},
    {"日期":"2026-09-02","周期":"本周","APP":"抖音","时长":1.0},
    {"日期":"2026-09-03","周期":"本周","APP":"抖音","时长":0.9},
    {"日期":"2026-09-04","周期":"本周","APP":"抖音","时长":0.8},
    {"日期":"2026-09-05","周期":"本周","APP":"抖音","时长":1.2},
    {"日期":"2026-09-06","周期":"本周","APP":"抖音","时长":0.7},
])

init_consume = pd.DataFrame([
    {"日期":"2026-08-26","周期":"上周","分类":"餐饮","金额":750},
    {"日期":"2026-08-26","周期":"上周","分类":"服饰","金额":600},
    {"日期":"2026-08-26","周期":"上周","分类":"数码","金额":450},
    {"日期":"2026-08-26","周期":"上周","分类":"文创","金额":300},
    {"日期":"2026-09-02","周期":"本周","分类":"餐饮","金额":680},
    {"日期":"2026-09-02","周期":"本周","分类":"服饰","金额":420},
    {"日期":"2026-09-02","周期":"本周","分类":"数码","金额":380},
    {"日期":"2026-09-02","周期":"本周","分类":"文创","金额":260},
])

init_news = pd.DataFrame([
    {"日期":"2026-08-26","周期":"上周","渠道":"短视频资讯","阅读量":15},
    {"日期":"2026-08-26","周期":"上周","渠道":"公众号","阅读量":22},
    {"日期":"2026-08-26","周期":"上周","渠道":"图文推文","阅读量":12},
    {"日期":"2026-08-26","周期":"上周","渠道":"新闻客户端","阅读量":10},
    {"日期":"2026-09-02","周期":"本周","渠道":"短视频资讯","阅读量":12},
    {"日期":"2026-09-02","周期":"本周","渠道":"公众号","阅读量":28},
    {"日期":"2026-09-02","周期":"本周","渠道":"图文推文","阅读量":16},
    {"日期":"2026-09-02","周期":"本周","渠道":"新闻客户端","阅读量":13},
])

# ====================== 数据文件路径（用于持久化） ======================
DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)  # 确保目录存在

SOCIAL_FILE = os.path.join(DATA_DIR, "social_data.csv")
CONSUME_FILE = os.path.join(DATA_DIR, "consume_data.csv")
NEWS_FILE = os.path.join(DATA_DIR, "news_data.csv")

# ====================== 加载函数：优先从文件读取，文件不存在则返回默认数据 ======================
def load_data(file_path, default_df):
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path, encoding='utf-8-sig')  # 兼容中文
        except Exception as e:
            st.error(f"读取 {file_path} 失败：{e}，使用默认数据")
            return default_df.copy()
    else:
        return default_df.copy()

def save_data(df, file_path):
    """将DataFrame保存为CSV文件"""
    try:
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
    except Exception as e:
        st.error(f"保存数据到 {file_path} 失败：{e}")

# ====================== 初始化 session_state（从文件加载） ======================
if "social_data" not in st.session_state:
    st.session_state.social_data = load_data(SOCIAL_FILE, init_social)
if "consume_data" not in st.session_state:
    st.session_state.consume_data = load_data(CONSUME_FILE, init_consume)
if "news_data" not in st.session_state:
    st.session_state.news_data = load_data(NEWS_FILE, init_news)

# 其他状态初始化
if "page" not in st.session_state:
    st.session_state.page = "home"
if "account_book" not in st.session_state:
    st.session_state.account_book = pd.DataFrame(columns=["日期","类型","分类","金额","备注"])
if "schedule" not in st.session_state:
    st.session_state.schedule = pd.DataFrame(columns=["日期","事项","状态"])
if "save_goal" not in st.session_state:
    st.session_state.save_goal = {
        "开启":False,
        "目标名称":"暑期旅游存钱",
        "目标总金额":5000,
        "已存金额":1800,
        "目标截止日期":date(2026,9,30)
    }

# ====================== 侧边导航 ======================
with st.sidebar:
    st.title("📱 功能导航")
    page = st.radio("模块选择",[
        "🏠 数据总览",
        "🎮 社交娱乐分析",
        "🛒 消费&存钱目标",
        "📰 资讯阅读分析",
        "🧠 习惯评估",
        "📒 每日记账系统",
        "📅 日程计划",
        "⚙ 数据上传设置"
    ])
    st.session_state.page = page

    # 显示数据来源状态
    if os.path.exists(SOCIAL_FILE) or os.path.exists(CONSUME_FILE) or os.path.exists(NEWS_FILE):
        st.sidebar.success("当前使用：自定义数据（已保存）")
    else:
        st.sidebar.info("当前使用：默认模拟数据")

# ====================== 1. 首页（折线图每日日期、柱状图周对比） ======================
if st.session_state.page == "🏠 数据总览":
    st.title("📊 全维度数字生活数据总览")

    st.subheader("📈 社交APP每日使用时长时序趋势")
    fig_s = px.line(st.session_state.social_data, x="日期", y="时长", color="APP", markers=True,
                    title="上周/本周 每日APP使用时长变化趋势")
    st.plotly_chart(fig_s, use_container_width=True)

    st.subheader("💰 两周消费金额对比")
    fig_c = px.bar(st.session_state.consume_data, x="周期", y="金额", color="分类", barmode="group",
                    title="上周/本周 各类消费金额对比")
    st.plotly_chart(fig_c, use_container_width=True)

    st.subheader("📰 资讯阅读量对比")
    fig_n = px.bar(st.session_state.news_data, x="周期", y="阅读量", color="渠道", barmode="group",
                    title="上周/本周 各渠道阅读量对比")
    st.plotly_chart(fig_n, use_container_width=True)

# ====================== 2. 社交娱乐分析 ======================
elif st.session_state.page == "🎮 社交娱乐分析":
    st.title("🎮 社交娱乐行为分析")
    df = st.session_state.social_data
    fig = px.bar(df, x="APP", y="时长", color="周期", barmode="group", title="上周/本周 APP使用时长对比")
    st.plotly_chart(fig, use_container_width=True)

    week_df = df.groupby("周期")["时长"].sum().reset_index()
    this_week = week_df[week_df["周期"]=="本周"]["时长"].values[0]
    last_week = week_df[week_df["周期"]=="上周"]["时长"].values[0]
    diff = round(this_week - last_week,2)

    if diff < 0:
        st.success(f"✅ 本周娱乐总时长较上周减少 {abs(diff)}h，时间管控效果良好！")
    else:
        st.warning(f"⚠️ 本周娱乐总时长较上周增加 {diff}h，需适当节制碎片化娱乐！")

# ====================== 3. 消费分析 + 存钱目标 ======================
elif st.session_state.page == "🛒 消费&存钱目标":
    st.title("🛒 消费分析 & 🎯 心愿存钱目标")

    st.subheader("🎯 我的存钱目标")
    goal = st.session_state.save_goal
    goal["开启"] = st.checkbox("开启存钱目标管理", True)

    if goal["开启"]:
        goal["目标名称"] = st.text_input("目标名称", goal["目标名称"])
        goal["目标总金额"] = st.number_input("目标总金额", min_value=0, value=goal["目标总金额"])
        goal["已存金额"] = st.number_input("当前已存金额", min_value=0, value=goal["已存金额"])
        goal["目标截止日期"] = st.date_input("计划完成日期", goal["目标截止日期"])

        if goal["目标总金额"] > 0:
            progress = goal["已存金额"] / goal["目标总金额"] * 100
            remain = goal["目标总金额"] - goal["已存金额"]
            st.progress(int(progress))
            st.success(f"✅ 存钱进度：{progress:.1f}% | 已存：{goal['已存金额']} 元 | 还差：{remain} 元")

            total_consume = st.session_state.consume_data["金额"].sum()
            st.warning(f"💡 本期总消费 {total_consume} 元，为完成【{goal['目标名称']}】，建议严控服饰、数码非刚需消费！")

    st.subheader("📊 本期消费结构分布")
    fig = px.pie(st.session_state.consume_data, values="金额", names="分类", title="消费占比可视化")
    st.plotly_chart(fig, use_container_width=True)

# ====================== 4. 资讯阅读分析 ======================
elif st.session_state.page == "📰 资讯阅读分析":
    st.title("📰 资讯阅读行为分析")
    df = st.session_state.news_data
    fig = px.bar(df, x="渠道", y="阅读量", color="周期", barmode="group", title="上周/本周 资讯阅读量对比")
    st.plotly_chart(fig, use_container_width=True)

    short_read = df[df["渠道"]=="短视频资讯"]["阅读量"].sum()
    long_read = df[df["渠道"].isin(["图文推文","新闻客户端"])]["阅读量"].sum()
    if short_read > long_read:
        st.warning("⚠️ 短视频浅层阅读占比偏高，深度资讯阅读不足，建议增加长文阅读！")
    else:
        st.success("✅ 深度阅读占比良好，信息获取质量较高！")

# ====================== 5. 习惯评估 ======================
elif st.session_state.page == "🧠 习惯评估":
    st.title("🧠 数字习惯综合评估")
    t = st.slider("时间自控得分",0,100,65)
    c = st.slider("消费理性得分",0,100,70)
    r = st.slider("资讯质量得分",0,100,62)
    avg = round((t+c+r)/3,1)
    st.metric("综合习惯得分",f"{avg} 分")

    fig = go.Figure(go.Scatterpolar(
        r=[t,c,r],
        theta=["时间自控","消费理性","资讯质量"],
        fill="toself",
        marker_color="#1f77b4"
    ))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0,100])), height=400)
    st.plotly_chart(fig, use_container_width=True)

    comp_df = pd.DataFrame({
        "维度":["时间自控","消费理性","资讯质量"],
        "上期":[60,68,55],
        "本期":[t,c,r]
    })
    st.plotly_chart(px.bar(comp_df,x="维度",y=["上期","本期"],barmode="group",title="习惯得分往期对比"),use_container_width=True)

# ====================== 6. 每日记账系统 ======================
elif st.session_state.page == "📒 每日记账系统":
    st.title("📒 个人每日记账系统")
    st.divider()

    d = st.date_input("选择日期")
    typ = st.selectbox("收支类型",["收入","支出"])
    cate = st.selectbox("分类",["餐饮","服饰","数码","娱乐","工资","红包","其他"])
    money = st.number_input("金额",0.0)
    note = st.text_input("备注")

    if st.button("✅ 保存记账"):
        new_row = pd.DataFrame({"日期":[d],"类型":[typ],"分类":[cate],"金额":[money],"备注":[note]})
        st.session_state.account_book = pd.concat([st.session_state.account_book,new_row],ignore_index=True)
        st.success("记账成功！")

    st.divider()
    st.subheader("📋 记账记录 & 收支统计")
    st.dataframe(st.session_state.account_book, use_container_width=True)

    if not st.session_state.account_book.empty:
        in_total = st.session_state.account_book[st.session_state.account_book["类型"]=="收入"]["金额"].sum()
        out_total = st.session_state.account_book[st.session_state.account_book["类型"]=="支出"]["金额"].sum()
        st.metric("总收入",f"{in_total} 元")
        st.metric("总支出",f"{out_total} 元")
        st.metric("当期结余",f"{in_total-out_total} 元")

# ====================== 7. 日程计划 ======================
elif st.session_state.page == "📅 日程计划":
    st.title("📅 每日行程计划管理")
    st.divider()

    d = st.date_input("计划日期")
    task = st.text_input("今日行程/待办事项")
    if st.button("➕ 添加行程"):
        new_task = pd.DataFrame({"日期":[d],"事项":[task],"状态":["未完成"]})
        st.session_state.schedule = pd.concat([st.session_state.schedule,new_task],ignore_index=True)
        st.success("行程添加成功！")

    st.divider()
    st.subheader("📋 我的全部行程（可修改完成状态）")

    if not st.session_state.schedule.empty:
        for idx, row in st.session_state.schedule.iterrows():
            col1,col2,col3 = st.columns([2,5,3])
            col1.write(row["日期"])
            col2.write(row["事项"])
            status = col3.selectbox("状态",["未完成","已完成"], index=0 if row["状态"]=="未完成" else 1, key=f"st_{idx}")
            st.session_state.schedule.loc[idx,"状态"] = status

        total = len(st.session_state.schedule)
        done = len(st.session_state.schedule[st.session_state.schedule["状态"]=="已完成"])
        st.success(f"✅ 行程完成率：{done}/{total}")
    else:
        st.info("暂无行程计划，可上方添加！")

# ====================== 8. 数据上传设置（支持持久化） ======================
elif st.session_state.page == "⚙ 数据上传设置":
    st.title("⚙ 自定义数据上传（数据将自动保存）")

    up_type = st.selectbox("上传数据类型",["社交娱乐","线上消费","资讯阅读"])
    file = st.file_uploader("上传CSV/Excel文件",type=["csv","xlsx"])

    if file:
        # 兼容 Excel / CSV
        if file.name.endswith(".xlsx"):
            df = pd.read_excel(file, engine="openpyxl")
        else:
            df = pd.read_csv(file)

        st.dataframe(df, use_container_width=True)

        # 列名检查（可选）
        required_cols = {
            "社交娱乐": ["日期","周期","APP","时长"],
            "线上消费": ["日期","周期","分类","金额"],
            "资讯阅读": ["日期","周期","渠道","阅读量"]
        }
        missing = [c for c in required_cols[up_type] if c not in df.columns]
        if missing:
            st.error(f"上传文件缺少必需列：{missing}，请检查表头！")
        else:
            # 覆盖数据 + 保存到本地文件
            if up_type == "社交娱乐":
                st.session_state.social_data = df.copy()
                save_data(st.session_state.social_data, SOCIAL_FILE)
            elif up_type == "线上消费":
                st.session_state.consume_data = df.copy()
                save_data(st.session_state.consume_data, CONSUME_FILE)
            elif up_type == "资讯阅读":
                st.session_state.news_data = df.copy()
                save_data(st.session_state.news_data, NEWS_FILE)
            st.success("✅ 数据上传成功！已自动保存，刷新页面或重启应用也不会丢失。")

    # 恢复默认数据（需要确认）
    st.divider()
    st.warning("如需恢复默认模拟数据，请先勾选确认，然后点击按钮。")
    confirm_reset = st.checkbox("我确认要删除自定义数据并恢复默认数据", key="confirm_reset")
    if st.button("🔄 恢复默认模拟数据", disabled=not confirm_reset):
        st.session_state.social_data = init_social.copy()
        st.session_state.consume_data = init_consume.copy()
        st.session_state.news_data = init_news.copy()
        # 删除本地保存文件（如果存在）
        for f in [SOCIAL_FILE, CONSUME_FILE, NEWS_FILE]:
            if os.path.exists(f):
                os.remove(f)
        st.success("已恢复默认数据，并删除本地自定义数据文件。")
        st.rerun()