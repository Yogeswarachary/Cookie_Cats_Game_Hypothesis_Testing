import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy import stats

@st.cache_data
def load_data():
    """Load cookie_cats.csv directly from GitHub raw URL"""
    url = "https://raw.githubusercontent.com/Yogeswarachary/Cookie_Cats_Game_Hypothesis_Testing/main/CSV Data/cookie_cats.csv"
    
    try:
        df = pd.read_csv(url)
        st.success(f"Loaded {df.shape[0]:,} users")
        return df
    except Exception as e:
        st.error(f"❌ CSV load failed: {e}")
        st.stop()

df = load_data()
st.title("Cookie Cats – A/B Testing Dashboard")

# Sidebar
gate_a = st.sidebar.selectbox("Gate A", [30, 40], index=0)
gate_b = st.sidebar.selectbox("Gate B", [30, 40], index=1)

group_a = df[df['gate'] == gate_a]
group_b = df[df['gate'] == gate_b]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users", len(df))
col2.metric("Gate A Users", len(group_a))
col3.metric("Gate B Users", len(group_b))
col4.metric("Days", df['day'].nunique())

# Retention curves (go only - no px)
st.subheader("📊 Retention Curves")
retention_a = group_a.groupby('day')['user_id'].nunique().reset_index()
retention_b = group_b.groupby('day')['user_id'].nunique().reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x=retention_a['day'], y=retention_a['user_id'],
                        mode='lines+markers', name=f'Gate {gate_a}'))
fig.add_trace(go.Scatter(x=retention_b['day'], y=retention_b['user_id'],
                        mode='lines+markers', name=f'Gate {gate_b}'))
fig.update_layout(title="Retention by Day", xaxis_title="Day", yaxis_title="Users")
st.plotly_chart(fig, use_container_width=True)

# A/B Test
st.subheader("🔬 A/B Test Results (D1)")
d1_a = len(group_a[group_a['day'] == 1]) / len(group_a)
d1_b = len(group_b[group_b['day'] == 1]) / len(group_b)
st.metric("D1 Retention", f"{d1_a:.1%} vs {d1_b:.1%}")

# Chi-square
contingency = [[len(group_a[group_a['day'] == 1]), len(group_a)-len(group_a[group_a['day'] == 1])],
               [len(group_b[group_b['day'] == 1]), len(group_b)-len(group_b[group_b['day'] == 1])]]
chi2, p_value, *_ = stats.chi2_contingency(contingency)
col1, col2 = st.columns(2)
col1.metric("Chi²", f"{chi2:.2f}")
col2.metric("P‑Value", f"{p_value:.3f}", 
           delta="🟢 Significant" if p_value < 0.05 else "🔴 Not significant")

st.subheader("📋 Data Preview")
st.dataframe(df.head(10), use_container_width=True)
