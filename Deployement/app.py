"""🍪 Cookie Cats A/B Testing Dashboard – Streamlit App"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import chi2_contingency

# Load data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Yogeswarachary/Cookie_Cats_Game_Hypothesis_Testing/main/CSV%20Data/cookie_cats.csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip().str.lower()
    st.success(f"✅ Loaded {df.shape[0]:,} rows successfully!")
    return df

st.set_page_config(page_title="Cookie Cats A/B Test", layout="wide")
df = load_data()

st.title("🍪 Cookie Cats – A/B Testing Dashboard")

# Sidebar controls
gate_a = st.sidebar.selectbox("Gate A", [30, 40], index=0)
gate_b = st.sidebar.selectbox("Gate B", [40, 30], index=0)

if gate_a == gate_b:
    st.warning("⚠️ Gate A and Gate B are the same — choose different versions to compare.")
    st.stop()

# Filter data by version column
group_a = df[df["version"] == f"gate_{gate_a}"]
group_b = df[df["version"] == f"gate_{gate_b}"]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users", f"{len(df):,}")
col2.metric(f"Gate {gate_a} Users", f"{len(group_a):,}")
col3.metric(f"Gate {gate_b} Users", f"{len(group_b):,}")
col4.metric("Retention Metrics", "D1 / D7")


# Retention Comparison (Plot)
st.subheader("📊 Average Retention Rate")

ret_a1 = group_a["retention_1"].mean()
ret_a7 = group_a["retention_7"].mean()
ret_b1 = group_b["retention_1"].mean()
ret_b7 = group_b["retention_7"].mean()

fig = go.Figure(data=[
    go.Bar(name=f"Gate {gate_a}", x=["D1", "D7"], y=[ret_a1, ret_a7], marker_color="#1f77b4"),
    go.Bar(name=f"Gate {gate_b}", x=["D1", "D7"], y=[ret_b1, ret_b7], marker_color="#ff7f0e")
])
fig.update_layout(barmode='group', title="Retention Rate Comparison", yaxis_title="Retention Rate", xaxis_title="Day")
st.plotly_chart(fig, use_container_width=True)

# A/B Significance Test (Chi-square on D1 retention)
st.subheader("🔬 A/B Test Results (D1 Retention)")

contingency = [
    [group_a["retention_1"].sum(), len(group_a) - group_a["retention_1"].sum()],
    [group_b["retention_1"].sum(), len(group_b) - group_b["retention_1"].sum()]
]
chi2, p_value, _, _ = chi2_contingency(contingency)

col1, col2 = st.columns(2)
col1.metric("Chi² Statistic", f"{chi2:.2f}")
col2.metric("P-Value", f"{p_value:.3f}", delta="🟢 Significant" if p_value < 0.05 else "🔴 Not significant")

# Data preview
st.subheader("📋 Data Preview")
st.dataframe(df.head(10), use_container_width=True)
