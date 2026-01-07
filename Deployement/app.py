"""Cookie Cats A/B Testing - Deployement Ready"""

try:
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    from scipy import stats
    PLOTLY_AVAILABLE = True
except ImportError as e:
    st.error(f"Missing dependency: {e}")
    st.stop()

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Yogeswarachary/Cookie_Cats_Game_Hypothesis_Testing/main/CSV%20Data/cookie_cats.csv"

    df = pd.read_csv(url)
    return df

st.set_page_config(page_title="Cookie Cats A/B", layout="wide")
df = load_data()

st.title("🍪 Cookie Cats – A/B Testing Dashboard")

# Sidebar
gate_a = st.sidebar.selectbox("Gate A", [30, 40])
gate_b = st.sidebar.selectbox("Gate B", [30, 40])

group_a = df[df['version'] == f"gate_{gate_a}"]
group_b = df[df['version'] == f"gate_{gate_b}"]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users", f"{len(df):,}")
col2.metric("Gate {gate_a}", len(group_a))
col3.metric("Gate {gate_b}", len(group_b))
col4.metric("Days", df['day'].nunique())

# Retention Plot
st.subheader("📊 Retention Curves")
retention_a = group_a.groupby('day')['user_id'].nunique()
retention_b = group_b.groupby('day')['user_id'].nunique()

if PLOTLY_AVAILABLE:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(retention_a.index), y=retention_a.values,
                            mode='lines+markers', name=f'Gate {gate_a}'))
    fig.add_trace(go.Scatter(x=list(retention_b.index), y=retention_b.values,
                            mode='lines+markers', name=f'Gate {gate_b}'))
    fig.update_layout(title="Retention", xaxis_title="Day")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Plotly unavailable - metrics only")

# Stats
st.subheader("🔬 A/B Test (D1)")
d1_a = len(group_a[group_a['day'] == 1]) / len(group_a)
d1_b = len(group_b[group_b['day'] == 1]) / len(group_b)
st.metric("D1 Retention", f"{d1_a:.1%} → {d1_b:.1%}")

chi2, p = stats.chi2_contingency([
    [len(group_a[group_a['day'] == 1]), len(group_a)-len(group_a[group_a['day'] == 1])],
    [len(group_b[group_b['day'] == 1]), len(group_b)-len(group_b[group_b['day'] == 1])]
])[:2]

col1, col2 = st.columns(2)
col1.metric("Chi²", f"{chi2:.2f}")
col2.metric("P‑Value", f"{p:.3f}", 
           delta="🟢" if p < 0.05 else "🔴")

st.subheader("📋 Data")
st.dataframe(df.head(10))
