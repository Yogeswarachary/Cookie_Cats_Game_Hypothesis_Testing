import streamlit as st
import pandas as pd
# import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import io
import requests

@st.cache_data
def load_data():
    """Load cookie_cats.csv directly from GitHub raw URL"""
    url = "https://raw.githubusercontent.com/Yogeswarachary/Cookie_Cats_Game_Hypothesis_Testing/main/CSV Data/cookie_cats.csv"
    
    try:
        df = pd.read_csv(url)
        st.success(f"✅ Loaded {df.shape[0]:,} users from GitHub")
        return df
    except Exception as e:
        st.error(f"❌ Failed to load CSV: {e}")
        st.info("**Fix**: Check GitHub raw URL is public + correct")
        st.stop()

df = load_data()
st.title("🍪 Cookie Cats – A/B Testing Dashboard")

# Sidebar: Gate selector
gate_a = st.sidebar.selectbox("Gate A", [30, 40], index=0)
gate_b = st.sidebar.selectbox("Gate B", [30, 40], index=1)

# Filter data
group_a = df[df['gate'] == gate_a]
group_b = df[df['gate'] == gate_b]

# ========== KPI CARDS ==========
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Users", len(df))
with col2:
    st.metric("Gate A Users", len(group_a))
with col3:
    st.metric("Gate B Users", len(group_b))
with col4:
    st.metric("Days Tested", df['day'].nunique())

# ========== RETENTION CURVES ==========
st.subheader("📊 Retention by Day (D0-D7)")
retention_a = group_a.groupby('day')['user_id'].nunique().reset_index()
retention_b = group_b.groupby('day')['user_id'].nunique().reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=retention_a['day'], y=retention_a['user_id'],
    mode='lines+markers', name=f'Gate {gate_a}'
))
fig.add_trace(go.Scatter(
    x=retention_b['day'], y=retention_b['user_id'],
    mode='lines+markers', name=f'Gate {gate_b}'
))
fig.update_layout(title="Retention Curves", xaxis_title="Day", yaxis_title="Users")
st.plotly_chart(fig, use_container_width=True)

# ========== A/B TEST RESULTS ==========
st.subheader("🔬 Statistical Tests")

# D1 retention test
d1_a = len(group_a[group_a['day'] == 1]) / len(group_a)
d1_b = len(group_b[group_b['day'] == 1]) / len(group_b)

st.metric("D1 Retention A/B", f"{d1_a:.1%} vs {d1_b:.1%}")

# Chi-square test
contingency = [[len(group_a[group_a['day'] == 1]), len(group_a[group_a['day'] != 1])],
               [len(group_b[group_b['day'] == 1]), len(group_b[group_b['day'] != 1])]]
chi2, p_value = stats.chi2_contingency(contingency)[:2]

col1, col2 = st.columns(2)
col1.metric("Chi² Statistic", f"{chi2:.2f}")
col2.metric("P‑Value", f"{p_value:.3f}", 
           delta="Significant?" if p_value < 0.05 else "Not significant")

# Data preview
st.subheader("📋 Raw Data Preview")
st.dataframe(df.head(10))
