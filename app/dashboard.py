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
    ["business_name", "efficiency_score", "equity_score", "sustainability_score", "dominant_objective"]
].reset_index(drop=True)
top_df.index = top_df.index + 1

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
    hover_data=["business_name"],
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

# ── Budget Simulator ──────────────────────────────────────────────────────────
st.divider()
st.subheader("💰 Incentive Budget Simulator")
st.markdown("Adjust objective weights and total budget to simulate incentive allocation across businesses.")

col_w1, col_w2, col_w3 = st.columns(3)

with col_w1:
    w_efficiency = st.slider("Efficiency Weight (%)", 0, 100, 33)
with col_w2:
    w_equity = st.slider("Equity Weight (%)", 0, 100, 33)
with col_w3:
    w_sustainability = st.slider("Sustainability Weight (%)", 0, 100, 34)

total_weight = w_efficiency + w_equity + w_sustainability

if total_weight == 0:
    st.error("Weights cannot all be zero.")
else:
    if total_weight != 100:
        st.warning(f"Weights sum to {total_weight}%. They will be normalised automatically.")

    w_e = w_efficiency / total_weight
    w_q = w_equity / total_weight
    w_s = w_sustainability / total_weight

    df["composite_score"] = (
        w_e * df["efficiency_score"] +
        w_q * df["equity_score"] +
        w_s * df["sustainability_score"]
    )

    st.markdown("---")
    total_budget = st.number_input(
        "Total Incentive Budget (RM)",
        min_value=10000,
        max_value=10000000,
        value=500000,
        step=10000,
        format="%d"
    )

    top_n_budget = st.slider("Number of Businesses to Fund", 10, 500, 100, step=10)

    funded_df = df.nlargest(top_n_budget, "composite_score").copy()
    funded_df["allocation_rm"] = (
        funded_df["composite_score"] / funded_df["composite_score"].sum() * total_budget
    ).round(2)

    st.markdown("---")
    col_b1, col_b2, col_b3 = st.columns(3)
    col_b1.metric("Businesses Funded", f"{top_n_budget:,}")
    col_b2.metric("Avg Allocation (RM)", f"RM {funded_df['allocation_rm'].mean():,.2f}")
    col_b3.metric("Total Allocated (RM)", f"RM {funded_df['allocation_rm'].sum():,.2f}")

    st.subheader("Allocation Results")
    results_df = funded_df[["business_name", "efficiency_score", "equity_score",
                             "sustainability_score", "composite_score",
                             "dominant_objective", "allocation_rm"]].reset_index(drop=True)
    results_df.index = results_df.index + 1
    st.dataframe(results_df, use_container_width=True)

    st.subheader("Top 20 Businesses by Allocation")
    fig6 = px.bar(
        funded_df.head(20),
        x="business_name",
        y="allocation_rm",
        color="dominant_objective",
        title="Incentive Allocation per Business (Top 20)",
        labels={"allocation_rm": "Allocation (RM)", "business_name": "Business"},
        template="plotly_dark"
    )
    st.plotly_chart(fig6, use_container_width=True)