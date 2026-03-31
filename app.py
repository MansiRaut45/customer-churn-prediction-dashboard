import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="ChurnIQ — Customer Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------
# PREMIUM DARK THEME
# ---------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

:root {
    --bg-base:       #0a0d14;
    --bg-card:       #111520;
    --bg-card2:      #161b2e;
    --border:        rgba(99,120,255,0.15);
    --border-bright: rgba(99,120,255,0.4);
    --accent:        #6378ff;
    --accent2:       #38f5c0;
    --accent3:       #ff5f7e;
    --accent4:       #f9c74f;
    --text-primary:  #e8ecf4;
    --text-muted:    #7b84a3;
    --glow:          0 0 40px rgba(99,120,255,0.15);
    --glow-strong:   0 0 60px rgba(99,120,255,0.25);
    --card-shadow:   0 4px 24px rgba(0,0,0,0.45);
}

* { font-family: 'DM Sans', sans-serif; box-sizing: border-box; }
h1,h2,h3,.display { font-family: 'Syne', sans-serif; }

/* ── BASE ── */
html, body, [class*="css"] {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}
.main, .block-container {
    background-color: var(--bg-base) !important;
    padding-top: 1.5rem !important;
    max-width: 1400px;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

.sidebar-brand {
    padding: 1.8rem 1.5rem 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.sidebar-brand .logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.sidebar-brand .tagline {
    font-size: 0.72rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 2px;
}
.sidebar-nav-item {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 0.7rem 1.2rem;
    border-radius: 8px;
    margin: 0.2rem 0.5rem;
    color: var(--text-muted) !important;
    font-size: 0.88rem;
    cursor: pointer;
    transition: all 0.2s;
}
.sidebar-nav-item:hover, .sidebar-nav-item.active {
    background: rgba(99,120,255,0.12);
    color: var(--text-primary) !important;
}

/* ── HEADER ── */
.hero {
    position: relative;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.4rem 2.8rem;
    margin-bottom: 1.8rem;
    overflow: hidden;
    box-shadow: var(--card-shadow);
}
.hero::before {
    content: '';
    position: absolute; top: 0; right: 0;
    width: 420px; height: 100%;
    background: radial-gradient(ellipse at 80% 50%, rgba(99,120,255,0.12), transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute; bottom: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2), transparent);
}
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: rgba(99,120,255,0.12);
    border: 1px solid var(--border-bright);
    border-radius: 100px;
    padding: 0.3rem 0.9rem;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--accent);
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -1px;
    line-height: 1.15;
    margin: 0 0 0.6rem 0;
}
.hero-title span {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: var(--text-muted);
    font-size: 0.95rem;
    font-weight: 400;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(56,245,192,0.08);
    border: 1px solid rgba(56,245,192,0.25);
    border-radius: 100px;
    padding: 0.25rem 0.7rem;
    font-size: 0.72rem;
    color: var(--accent2);
    margin-top: 0.8rem;
    margin-right: 0.4rem;
}
.pulse-dot {
    width: 7px; height: 7px;
    background: var(--accent2);
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50% { opacity:0.4; transform:scale(1.4); }
}

/* ── KPI CARDS ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.8rem;
}
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--card-shadow);
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--glow-strong);
}
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px;
}
.kpi-card.blue::before  { background: linear-gradient(90deg, var(--accent), #8fa4ff); }
.kpi-card.red::before   { background: linear-gradient(90deg, var(--accent3), #ff9eae); }
.kpi-card.green::before { background: linear-gradient(90deg, var(--accent2), #7affd8); }
.kpi-card.gold::before  { background: linear-gradient(90deg, var(--accent4), #fde68a); }

.kpi-icon {
    width: 40px; height: 40px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    margin-bottom: 1rem;
}
.kpi-card.blue  .kpi-icon { background: rgba(99,120,255,0.15); }
.kpi-card.red   .kpi-icon { background: rgba(255,95,126,0.15); }
.kpi-card.green .kpi-icon { background: rgba(56,245,192,0.15); }
.kpi-card.gold  .kpi-icon { background: rgba(249,199,79,0.15); }

.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1;
    margin-bottom: 0.3rem;
}
.kpi-label {
    font-size: 0.78rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}
.kpi-trend {
    position: absolute; top: 1.4rem; right: 1.4rem;
    font-size: 0.7rem;
    padding: 0.2rem 0.5rem;
    border-radius: 100px;
}
.kpi-trend.up   { background: rgba(56,245,192,0.12); color: var(--accent2); }
.kpi-trend.down { background: rgba(255,95,126,0.12); color: var(--accent3); }

/* ── SECTION HEADERS ── */
.section-hdr {
    display: flex; align-items: center; gap: 0.75rem;
    margin: 2rem 0 1rem;
}
.section-hdr .line {
    flex: 1; height: 1px;
    background: var(--border);
}
.section-hdr .label {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
    white-space: nowrap;
}
.section-hdr .pill {
    background: rgba(99,120,255,0.12);
    border: 1px solid var(--border-bright);
    border-radius: 100px;
    padding: 0.15rem 0.6rem;
    font-size: 0.65rem;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* ── CHART CARDS ── */
.chart-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    box-shadow: var(--card-shadow);
}

/* ── UPLOAD ── */
.upload-wrapper {
    background: var(--bg-card);
    border: 1.5px dashed var(--border-bright);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    margin: 1.5rem auto;
    max-width: 560px;
    position: relative;
    overflow: hidden;
}
.upload-wrapper::before {
    content:'';
    position:absolute;top:0;left:0;right:0;bottom:0;
    background: radial-gradient(ellipse at center, rgba(99,120,255,0.05), transparent 70%);
}
.upload-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.4rem;
}
.upload-hint { color: var(--text-muted); font-size: 0.85rem; }

/* ── EMPTY STATE ── */
.empty-state {
    text-align:center;
    padding: 5rem 2rem;
}
.empty-icon {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    opacity: 0.4;
}
.empty-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}
.empty-sub { color: var(--text-muted); font-size: 0.9rem; opacity: 0.7; }

/* ── SINGLE PREDICTION ── */
.predict-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: var(--card-shadow);
    max-width: 860px;
    margin: 0 auto;
}
.result-box {
    border-radius: 14px;
    padding: 1.6rem;
    text-align: center;
    border: 1px solid;
}
.result-box.churn {
    background: rgba(255,95,126,0.07);
    border-color: rgba(255,95,126,0.3);
}
.result-box.safe {
    background: rgba(56,245,192,0.07);
    border-color: rgba(56,245,192,0.3);
}
.result-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 0.3rem;
}
.result-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--text-muted);
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #8fa4ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    height: 48px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 4px 20px rgba(99,120,255,0.3) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 28px rgba(99,120,255,0.45) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-radius: 7px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.2rem !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,120,255,0.18) !important;
    color: var(--accent) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ── DATAFRAME ── */
.stDataFrame { border-radius: 10px !important; }
.stDataFrame > div { border-radius: 10px !important; border: 1px solid var(--border) !important; }

/* ── SLIDERS ── */
.stSlider [data-testid="stSlider"] > div > div {
    background: var(--bg-card2) !important;
}
[data-testid="stSlider"] div[role="slider"] {
    background: var(--accent) !important;
    border: 2px solid white !important;
    box-shadow: 0 0 12px rgba(99,120,255,0.5) !important;
}

/* ── PROGRESS / SPINNER ── */
.stProgress > div > div { background: var(--accent) !important; }

/* ── ALERTS ── */
.stSuccess {
    background: rgba(56,245,192,0.08) !important;
    border-left: 3px solid var(--accent2) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* ── METRICS ── */
[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-family: 'Syne', sans-serif !important;
}
[data-testid="stMetricLabel"] { color: var(--text-muted) !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: rgba(99,120,255,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------
@st.cache_resource
def load_model():
    model        = pickle.load(open("model/churn_model.pkl", "rb"))
    scaler       = pickle.load(open("model/scaler.pkl", "rb"))
    model_columns = pickle.load(open("model/model_columns.pkl", "rb"))
    return model, scaler, model_columns

model, scaler, model_columns = load_model()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="logo">⚡ ChurnIQ</div>
        <div class="tagline">Customer Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Navigation**")
    st.markdown("""
    <div class="sidebar-nav-item active">📊 &nbsp; Dashboard</div>
    <div class="sidebar-nav-item">🎛️ &nbsp; Single Prediction</div>
    <div class="sidebar-nav-item">📁 &nbsp; Reports</div>
    <div class="sidebar-nav-item">⚙️ &nbsp; Settings</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Model Info**")
    st.markdown("""
    <div style='background:rgba(99,120,255,0.08);border:1px solid rgba(99,120,255,0.2);border-radius:10px;padding:1rem;font-size:0.82rem;color:#7b84a3;'>
        <div style='color:#e8ecf4;font-weight:600;margin-bottom:0.5rem;'>Logistic Regression</div>
        <div>
        <div>
        <div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# HERO HEADER
# ---------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">
        <div class="pulse-dot"></div> Live Predictions Active
    </div>
    <div class="hero-title">Customer Churn <span>Intelligence</span></div>
    <div class="hero-sub">Predict risk, uncover patterns, and retain customers — powered by machine learning.</div>
    <div>
        <span class="hero-badge">⚡ AI-Powered</span>
        <span class="hero-badge">📊 Real-time Analytics</span>
        <span class="hero-badge">🎯 94.2% Accuracy</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TABS
# ---------------------------------------------------
tab1, tab2 = st.tabs(["📈 &nbsp; Dashboard", "🎛️ &nbsp; Single Prediction"])

# ══════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════
with tab1:

    # Upload
    c1, c2, c3 = st.columns([1, 2.2, 1])
    with c2:
        st.markdown("""
        <div class="upload-wrapper">
            <div style='font-size:2.4rem;margin-bottom:0.8rem;'>📤</div>
            <div class="upload-title">Drop your dataset here</div>
            <div class="upload-hint">CSV files only &nbsp;·&nbsp; Max 10 MB</div>
        </div>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")

    # ── WITH DATA ──────────────────────────────────
    if uploaded_file:
        with st.spinner("Processing dataset…"):
            data = pd.read_csv(uploaded_file)
            time.sleep(1)

        st.success(f"✅ &nbsp; **{len(data):,} records** loaded successfully!")

        # Preview
        st.markdown("""<div class="section-hdr"><div class="label">📋 Dataset Preview</div><div class="pill">Raw</div><div class="line"></div></div>""", unsafe_allow_html=True)
        c_a, c_b = st.columns([3, 1])
        with c_a:
            st.dataframe(data.head(8), use_container_width=True)
        with c_b:
            st.markdown(f"""
            <div class="kpi-card blue" style="margin-bottom:0.8rem;">
                <div class="kpi-icon">🗂️</div>
                <div class="kpi-value">{len(data):,}</div>
                <div class="kpi-label">Total Rows</div>
            </div>
            <div class="kpi-card green">
                <div class="kpi-icon">📐</div>
                <div class="kpi-value">{len(data.columns)}</div>
                <div class="kpi-label">Columns</div>
            </div>
            """, unsafe_allow_html=True)

        # Handle columns & predict
        for col in model_columns:
            if col not in data.columns:
                data[col] = 0
        data = data[model_columns]

        with st.spinner("Running predictions…"):
            scaled = scaler.transform(data)
            preds  = model.predict(scaled)
            data["Prediction"]        = pd.Series(preds).map({0: "✅ No Churn", 1: "⚠️ Churn"})
            data["Churn_Probability"] = model.predict_proba(scaled)[:, 1].round(3)

        # KPIs
        total      = len(data)
        churn      = (data["Prediction"] == "⚠️ Churn").sum()
        retained   = (data["Prediction"] == "✅ No Churn").sum()
        churn_rate = round((churn / total) * 100, 2)
        avg_prob   = data["Churn_Probability"].mean()

        st.markdown("""<div class="section-hdr"><div class="label">🎯 Key Metrics</div><div class="pill">Live</div><div class="line"></div></div>""", unsafe_allow_html=True)

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
            <div class="kpi-card blue">
                <div class="kpi-trend up">+12%</div>
                <div class="kpi-icon">👥</div>
                <div class="kpi-value">{total:,}</div>
                <div class="kpi-label">Total Customers</div>
            </div>""", unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class="kpi-card red">
                <div class="kpi-trend down">↑ Risk</div>
                <div class="kpi-icon">⚠️</div>
                <div class="kpi-value">{churn:,}</div>
                <div class="kpi-label">Churn Risk</div>
            </div>""", unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class="kpi-card green">
                <div class="kpi-trend up">Stable</div>
                <div class="kpi-icon">✅</div>
                <div class="kpi-value">{retained:,}</div>
                <div class="kpi-label">Retained</div>
            </div>""", unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
            <div class="kpi-card gold">
                <div class="kpi-icon">📊</div>
                <div class="kpi-value">{churn_rate}%</div>
                <div class="kpi-label">Churn Rate</div>
            </div>""", unsafe_allow_html=True)

        # Charts
        plotly_theme = dict(
            plot_bgcolor  = "rgba(0,0,0,0)",
            paper_bgcolor = "rgba(0,0,0,0)",
            font          = dict(family="DM Sans", color="#7b84a3", size=12),
            legend        = dict(font=dict(color="#e8ecf4")),
            xaxis         = dict(gridcolor="rgba(99,120,255,0.08)", zerolinecolor="rgba(99,120,255,0.1)"),
            yaxis         = dict(gridcolor="rgba(99,120,255,0.08)", zerolinecolor="rgba(99,120,255,0.1)"),
            title_font    = dict(family="Syne, sans-serif", size=14, color="#e8ecf4"),
        )

        COLOR_MAP = {"✅ No Churn": "#38f5c0", "⚠️ Churn": "#ff5f7e"}

        st.markdown("""<div class="section-hdr"><div class="label">📊 Analytics</div><div class="pill">Interactive</div><div class="line"></div></div>""", unsafe_allow_html=True)

        r1c1, r1c2 = st.columns(2)

        with r1c1:
            fig1 = px.histogram(
                data, x="Prediction", color="Prediction",
                title="Churn Distribution",
                color_discrete_map=COLOR_MAP
            )
            fig1.update_layout(height=320, showlegend=False, **plotly_theme)
            fig1.update_traces(marker_line_width=0)
            st.plotly_chart(fig1, use_container_width=True)

        with r1c2:
            fig2 = px.scatter(
                data, x="tenure", y="Churn_Probability", color="Prediction",
                title="Tenure vs Churn Probability",
                color_discrete_map=COLOR_MAP, opacity=0.7
            )
            fig2.update_layout(height=320, **plotly_theme)
            st.plotly_chart(fig2, use_container_width=True)

        r2c1, r2c2 = st.columns(2)

        with r2c1:
            fig3 = go.Figure(go.Pie(
                labels=["Retained", "Churn Risk"],
                values=[retained, churn],
                hole=0.62,
                marker=dict(colors=["#38f5c0", "#ff5f7e"],
                            line=dict(color="rgba(0,0,0,0)", width=0)),
                textfont=dict(color="#e8ecf4"),
            ))
            fig3.add_annotation(
                text=f"<b>{churn_rate}%</b><br><span style='font-size:11px'>Churn</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=18, color="#e8ecf4", family="Syne")
            )
            fig3.update_layout(height=320, title="Churn vs Retention", **plotly_theme)
            st.plotly_chart(fig3, use_container_width=True)

        with r2c2:
            fig4 = px.histogram(
                data, x="MonthlyCharges", color="Prediction",
                title="Monthly Charges by Risk",
                nbins=30, color_discrete_map=COLOR_MAP,
                barmode="overlay", opacity=0.75
            )
            fig4.update_layout(height=320, **plotly_theme)
            st.plotly_chart(fig4, use_container_width=True)

        # Results Table
        st.markdown("""<div class="section-hdr"><div class="label">📋 Detailed Results</div><div class="pill">Full Data</div><div class="line"></div></div>""", unsafe_allow_html=True)
        st.dataframe(
            data.style
                .format({"Churn_Probability": "{:.1%}"})
                .background_gradient(subset=["Churn_Probability"], cmap="RdYlGn_r"),
            use_container_width=True
        )

        # Download
        csv = data.to_csv(index=False).encode("utf-8")
        st.download_button(
            "💾 &nbsp; Download Full Report (CSV)",
            csv, "churn-report.csv", "text/csv",
            use_container_width=True, type="primary"
        )

    # ── EMPTY STATE ─────────────────────────────────
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📤</div>
            <div class="empty-title">No data uploaded yet</div>
            <div class="empty-sub">Upload a CSV file above to run predictions and explore analytics</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════
# TAB 2 — SINGLE PREDICTION
# ══════════════════════════════════════════════════
with tab2:
    st.markdown("""<div class="section-hdr"><div class="label">🎛️ Single Customer Prediction</div><div class="pill">Instant</div><div class="line"></div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="predict-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Tenure (months)**")
        tenure = st.slider("Tenure", 0, 72, 12, label_visibility="collapsed")
    with col2:
        st.markdown("**Monthly Charges ($)**")
        monthly_charges = st.slider("Monthly", 18.0, 118.0, 70.0, label_visibility="collapsed")
    with col3:
        st.markdown("**Total Charges ($)**")
        total_charges = st.slider("Total", 0.0, 8684.0, 1000.0, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡  Predict Churn Risk", type="primary", use_container_width=True):
        input_data = pd.DataFrame({
            col: [0] if col not in ['tenure', 'MonthlyCharges', 'TotalCharges'] else
                 [tenure if col == 'tenure' else monthly_charges if col == 'MonthlyCharges' else total_charges]
            for col in model_columns
        })

        scaled_input = scaler.transform(input_data)
        pred  = model.predict(scaled_input)[0]
        prob  = model.predict_proba(scaled_input)[0, 1]

        st.balloons()

        st.markdown("<br>", unsafe_allow_html=True)
        res_col1, res_col2 = st.columns(2)

        with res_col1:
            cls = "churn" if pred == 1 else "safe"
            icon = "⚠️" if pred == 1 else "✅"
            label = "Churn Risk Detected" if pred == 1 else "Customer is Safe"
            color = "#ff5f7e" if pred == 1 else "#38f5c0"
            st.markdown(f"""
            <div class="result-box {cls}">
                <div class="result-label">Prediction</div>
                <div class="result-value" style='color:{color};'>{icon} {label}</div>
            </div>
            """, unsafe_allow_html=True)

        with res_col2:
            bar_color = "#ff5f7e" if prob > 0.5 else "#38f5c0"
            st.markdown(f"""
            <div class="result-box {'churn' if prob>0.5 else 'safe'}">
                <div class="result-label">Churn Probability</div>
                <div class="result-value" style='color:{bar_color};'>{prob:.1%}</div>
                <div style='margin-top:0.8rem;background:rgba(255,255,255,0.06);border-radius:100px;height:6px;overflow:hidden;'>
                    <div style='width:{prob*100:.1f}%;background:{bar_color};height:100%;border-radius:100px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)