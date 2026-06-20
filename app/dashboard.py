import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SME Incentive Allocation Engine",
    page_icon="🏭",
    layout="wide"
)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/scored_dataset.csv")
    return df

df = load_data()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏭 SME Incentive Allocation Engine")
st.markdown("Multi-objective optimization dashboard for informal sector business incentive distribution.")
st.divider()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.header("Filters")

objective = st.sidebar.selectbox(
    "Primary Objective",
    ["efficiency_score", "equity_score", "sustainability_score"],
    format_func=lambda x: x.replace("_score", "").capitalize()
)

top_n = st.sidebar.slider("Show Top N Businesses", min_value=10, max_value=200, value=50, step=10)

# ── KPI cards ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Businesses", f"{len(df):,}")
col2.metric("Avg Efficiency Score", f"{df['efficiency_score'].mean():.3f}")
col3.metric("Avg Equity Score", f"{df['equity_score'].mean():.3f}")
col4.metric("Avg Sustainability Score", f"{df['sustainability_score'].mean():.3f}")

st.divider()

# ── Top N table ───────────────────────────────────────────────────────────────
st.subheader(f"Top {top_n} Businesses by {objective.replace('_score','').capitalize()}")

top_df = df.nlargest(top_n, objective)[
    ["idstd", "efficiency_score", "equity_score", "sustainability_score", "dominant_objective"]
].reset_index(drop=True)

st.dataframe(top_df, use_container_width=True)

st.divider()

# ── Scatter: Efficiency vs Equity ─────────────────────────────────────────────
st.subheader("Pareto Trade-off: Efficiency vs Equity")

fig1 = px.scatter(
    df,
    x="efficiency_score",
    y="equity_score",
    color="dominant_objective",
    size="sustainability_score",
    hover_data=["idstd"],
    title="Efficiency vs Equity (size = Sustainability)",
    template="plotly_dark"
)
st.plotly_chart(fig1, use_container_width=True)

# ── Distribution ──────────────────────────────────────────────────────────────
st.subheader("Score Distributions")

col_a, col_b, col_c = st.columns(3)

with col_a:
    fig2 = px.histogram(df, x="efficiency_score", nbins=40,
                        title="Efficiency Score", template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

with col_b:
    fig3 = px.histogram(df, x="equity_score", nbins=40,
                        title="Equity Score", template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

with col_c:
    fig4 = px.histogram(df, x="sustainability_score", nbins=40,
                        title="Sustainability Score", template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)

# ── Dominant objective breakdown ──────────────────────────────────────────────
st.subheader("Dominant Objective Distribution")

fig5 = px.pie(
    df,
    names="dominant_objective",
    title="Businesses by Dominant Objective",
    template="plotly_dark"
)
st.plotly_chart(fig5, use_container_width=True)