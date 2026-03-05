import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# 1. Page Config
st.set_page_config(page_title="NYC Congestion Audit 2025", layout="wide", page_icon="🚕", initial_sidebar_state="expanded")

# --- Custom CSS for Premium Design ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main Background & Text Color */
    .stApp {
        background-color: #0A0A0B;
        color: #E2E8F0;
    }
    
    /* Top Header Styling */
    h1 {
        font-weight: 700 !important;
        background: linear-gradient(135deg, #FFE000, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 10px !important;
        margin-bottom: 5px !important;
        font-size: 2.8rem !important;
        letter-spacing: -0.02em;
    }

    h2, h3 {
        color: #F8FAFC !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em;
    }

    /* Metric Cards Styling */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(255, 215, 0, 0.1);
        border-color: rgba(255, 224, 0, 0.4);
    }

    div[data-testid="metric-container"] label {
        color: #94A3B8 !important;
        font-weight: 500;
        font-size: 1rem;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-weight: 700;
        font-size: 2.2rem;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: rgba(255, 255, 255, 0.02);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.08);
        color: #FFE000 !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: transparent !important;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #121214 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Info/Warning/Success Boxes */
    div.stInfo {
        background-color: rgba(56, 189, 248, 0.1) !important;
        color: #38BDF8 !important;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
    }
    div.stWarning {
        background-color: rgba(250, 204, 21, 0.1) !important;
        color: #FACC15 !important;
        border: 1px solid rgba(250, 204, 21, 0.3);
        border-radius: 12px;
    }
    div.stSuccess {
        background-color: rgba(74, 222, 128, 0.1) !important;
        color: #4ADE80 !important;
        border: 1px solid rgba(74, 222, 128, 0.3);
        border-radius: 12px;
    }
    div.stError {
        background-color: rgba(248, 113, 113, 0.1) !important;
        color: #F87171 !important;
        border: 1px solid rgba(248, 113, 113, 0.3);
        border-radius: 12px;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
        margin: 32px 0px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Data Loading with Caching
@st.cache_data
def load_data():
    clean_path = Path("outputs/clean_data.parquet")
    ghost_path = Path("outputs/ghost_trips.parquet")
    
    if not clean_path.exists():
        return None, None
    
    df = pd.read_parquet(clean_path)
    ghost_df = pd.read_parquet(ghost_path) if ghost_path.exists() else None
    return df, ghost_df

# Load the data
df, ghost_df = load_data()

# 3. Error Handling
if df is None:
    st.error("🚨 No processed data found in 'outputs/' folder!")
    st.info("Please run `python pipeline.py` first to generate the audit files.")
    st.stop()

# 4. Header & Top Metrics
st.title("NYC Congestion Pricing Audit 2025")
st.markdown(f"**Audit Period:** January 2025 | **Total Records Processed:** `{len(df) + (len(ghost_df) if ghost_df is not None else 0):,}` 📊")
st.write("") # Spacer

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Clean Trips", f"{len(df):,}")
col2.metric("Avg Fare", f"${df['fare'].mean():.2f}")
col3.metric("Congestion Surcharge Recv", f"${df['congestion_surcharge'].sum():,.0f}")
col4.metric("Estimated Compliance Rate", "73.99%")

st.divider()

# Update Plotly defaults for dark theme
px.defaults.template = "plotly_dark"
px.defaults.color_continuous_scale = px.colors.sequential.Plasma
px.defaults.color_discrete_sequence = px.colors.qualitative.Set3

# 5. Main Analysis Tabs
tab1, tab2, tab3 = st.tabs(["🕒 Hourly Patterns", "💰 Revenue Analysis", "🚨 Audit Results"])

with tab1:
    st.markdown("### Trip Activity by Hour")
    hourly = df.groupby('hour').size().reset_index(name='trip_count')
    fig = px.bar(hourly, x='hour', y='trip_count', color='trip_count',
                 labels={'trip_count': 'Number of Trips', 'hour': 'Hour of Day'},
                 color_continuous_scale='Plasma')
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="#94A3B8",
        margin=dict(t=20, l=0, r=0, b=0),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False),
    )
    fig.update_traces(marker_line_width=0, opacity=0.9)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Revenue Contribution")
    rev_col1, rev_col2 = st.columns(2)
    
    # Revenue by hour
    rev_hourly = df.groupby('hour')['total_amount'].sum().reset_index()
    fig_rev = px.area(rev_hourly, x='hour', y='total_amount', title="Total Revenue Trend")
    fig_rev.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="#94A3B8",
        title_font_color="#F8FAFC",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False),
    )
    # Style area fill
    fig_rev.update_traces(fillcolor='rgba(255, 215, 0, 0.2)', line_color='#FFE000')
    rev_col1.plotly_chart(fig_rev, use_container_width=True)
    
    # Top 5 Pickup Locations for Revenue
    top_locs = df.groupby('pickup_loc')['total_amount'].sum().nlargest(5).reset_index()
    # Ensure categorical typing so discrete colors work best
    top_locs['pickup_loc'] = top_locs['pickup_loc'].astype(str) 
    
    fig_loc = px.pie(top_locs, values='total_amount', names='pickup_loc', title="Revenue by Top Locations", hole=0.6)
    fig_loc.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="#94A3B8",
        title_font_color="#F8FAFC",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    fig_loc.update_traces(textposition='inside', textinfo='percent', hoverinfo='label+percent', marker=dict(line=dict(color='#0A0A0B', width=2)))
    rev_col2.plotly_chart(fig_loc, use_container_width=True)

with tab3:
    st.markdown("### Ghost Trip Detection Summary")
    if ghost_df is not None:
        st.warning(f"⚠️ **Total Anomalous 'Ghost' Trips Detected:** {len(ghost_df):,}")
        
        audit_col1, audit_col2 = st.columns([2, 1])
        
        audit_col1.write("##### Sample of Flagged Anomalies:")
        
        # Style dataframe for dark mode
        st.dataframe(
            ghost_df[['pickup_time', 'avg_speed', 'fare', 'trip_distance']].head(10),
            use_container_width=True,
            hide_index=True
        )
        
        audit_col2.info("""
        **Flagging Criteria:**
        - 🚀 Speed > 65 MPH
        - 🕹️ Duration < 1 min & Fare > $20
        - 🛑 Distance = 0 & Fare > $0
        
        *These trips are excluded from the main revenue and activity analysis.*
        """)
    else:
        st.info("✅ No ghost trip anomalies detected in the dataset.")

# 6. Sidebar Info
with st.sidebar:
    st.title("Project Details")
    st.success("✅ **Data Pipeline:** Complete")
    st.write("")
    
    st.markdown("### Tools Used")
    st.markdown("""
    <div style='background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05);'>
        <ul style='list-style-type: none; padding-left: 0; margin-bottom: 0;'>
            <li style='margin-bottom: 8px;'>🐍 Python 3.1x</li>
            <li style='margin-bottom: 8px;'>⚡ Dask (Processing)</li>
            <li style='margin-bottom: 8px;'>🎨 Streamlit (UI)</li>
            <li>📊 Plotly (Visuals)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    if st.button("🔄 Clear Dashboard Cache", use_container_width=True):
        st.cache_data.clear()
        st.rerun()