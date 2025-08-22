import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Page configuration for better layout
st.set_page_config(
    page_title="Nigerian Exchange Rate Dashboard",
    page_icon="🇳🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: fadeInUp 1s ease-out;
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .metric-card h2 {
        margin: 0 0 0.5rem 0;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .metric-card p {
        margin: 0;
        opacity: 0.8;
        font-size: 0.9rem;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Specific styling for the get rate button */
    #get_rate_btn {
        background: linear-gradient(90deg, #6c757d 0%, #495057 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: normal !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(108, 117, 125, 0.2) !important;
        min-width: 120px !important;
    }
    
    #get_rate_btn:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(108, 117, 125, 0.3) !important;
        background: linear-gradient(90deg, #5a6268 0%, #343a40 100%) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Success and info boxes */
    .stSuccess {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(23, 162, 184, 0.3);
    }
    
    /* Warning styling */
    .stWarning {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
    }
    
    /* Error styling */
    .stError {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
    }
    
    /* Chart container */
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    /* Date checker section styling */
    .date-checker-section {
        background: rgba(248, 249, 250, 0.8);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }
    
    .date-checker-section .stDateInput {
        margin: 1rem 0;
    }
    
    .date-checker-section .stButton {
        margin: 1rem 0;
    }
    
    .date-checker-section .stButton > button {
        height: 3rem;
        font-size: 1.1rem;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        .metric-card {
            padding: 1rem;
        }
        .metric-card h2 {
            font-size: 1.5rem;
        }
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Fetch all rows from Supabase with pagination
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_exchange_data():
    all_data = []
    page = 0
    page_size = 1000  # max rows per request
    while True:
        res = supabase.table("exchange_rates").select("*").range(page*page_size, (page+1)*page_size - 1).execute()
        if not res.data:
            break
        all_data.extend(res.data)
        page += 1
    
    df = pd.DataFrame(all_data)
    df['rate_date'] = pd.to_datetime(df['rate_date'], errors='coerce')
    df = df.rename(columns={'rate_date': 'Date', 'rate': 'ExchangeRate'})
    df = df.sort_values('Date').reset_index(drop=True)
    return df

df = fetch_exchange_data()

# Initialize session state for sidebar visibility and graph display
if 'sidebar_visible' not in st.session_state:
    st.session_state.sidebar_visible = True
if 'show_graph_requested' not in st.session_state:
    st.session_state.show_graph_requested = False
if 'selected_start_year' not in st.session_state:
    st.session_state.selected_start_year = df["Date"].dt.year.min()
if 'selected_end_year' not in st.session_state:
    st.session_state.selected_end_year = df["Date"].dt.year.max()

# Main header with enhanced styling
st.markdown('<h1 class="main-header">Nigerian Exchange Rate Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Real-time exchange rate visualization and analysis for NGN/USD</p>', unsafe_allow_html=True)

# Top metrics dashboard
st.markdown('<h2 class="section-header">📊 Live Exchange Rate Metrics</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    latest_rate = df['ExchangeRate'].iloc[-1]
    st.markdown(f"""
    <div class="metric-card">
        <h3>Current Rate</h3>
        <h2>₦{latest_rate:.2f}</h2>
        <p>Latest USD Rate</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    rate_change = df['ExchangeRate'].iloc[-1] - df['ExchangeRate'].iloc[-2] if len(df) > 1 else 0
    change_icon = "📈" if rate_change >= 0 else "📉"
    change_color = "#00ff88" if rate_change >= 0 else "#ff6b6b"
    st.markdown(f"""
    <div class="metric-card">
        <h3>Daily Change</h3>
        <h2>{change_icon} ₦{rate_change:.2f}</h2>
        <p style="color: {change_color};">vs Previous Day</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_rate = df['ExchangeRate'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <h3>Average Rate</h3>
        <h2>₦{avg_rate:.2f}</h2>
        <p>Historical Average</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    date_range = (df['Date'].max() - df['Date'].min()).days
    st.markdown(f"""
    <div class="metric-card">
        <h3>Data Span</h3>
        <h2>{date_range}</h2>
        <p>Days of Data</p>
    </div>
    """, unsafe_allow_html=True)

# Enhanced sidebar with better styling
# Sidebar filter with enhanced styling
if st.session_state.sidebar_visible:
    st.sidebar.markdown("### 📅 Filter by Year")
    min_year = df["Date"].dt.year.min()
    max_year = df["Date"].dt.year.max()

    # Add some spacing and styling
    st.sidebar.markdown("---")

    # Create year options for dropdowns to prevent errors
    year_options = list(range(min_year, max_year + 1))

    # Use selectbox instead of text input for better error prevention
    start_year = st.sidebar.selectbox(
        "Start Year", 
        options=year_options,
        index=0,
        key="start_year_selector",
        help="Select the start year for filtering"
    )
    
    # Store selected year in session state
    st.session_state.selected_start_year = start_year

    end_year = st.sidebar.selectbox(
        "End Year", 
        options=year_options,
        index=len(year_options) - 1,
        key="end_year_selector",
        help="Select the end year for filtering"
    )
    
    # Store selected year in session state
    st.session_state.selected_end_year = end_year

    # Validation with user-friendly messages
    if start_year > end_year:
        st.sidebar.warning("⚠️ **Invalid Range**: Start year cannot be after end year")
        st.sidebar.info("💡 **Tip**: Start year should be earlier than or equal to end year")
    else:
        st.sidebar.success(f"✅ **Valid Range**: {start_year} to {end_year}")

    st.sidebar.markdown("---")
    show_graph = st.sidebar.button("🚀 Show Exchange Rate Graph", use_container_width=True)

    # Toggle sidebar visibility when graph button is clicked
    if show_graph:
        st.session_state.sidebar_visible = False
        st.session_state.show_graph_requested = True
        st.rerun()
else:
    # Show a button to reopen the sidebar
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📱 Reopen Controls", use_container_width=True):
            st.session_state.sidebar_visible = True
            st.rerun()

# Enhanced graph section
if st.session_state.show_graph_requested:
    # Use stored year values from session state
    start_year = st.session_state.selected_start_year
    end_year = st.session_state.selected_end_year
    
    # Add a button to close the graph and return to normal view
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("❌ Close Graph", use_container_width=True):
            st.session_state.show_graph_requested = False
            st.rerun()
    
    # Additional validation before showing graph
    if start_year > end_year:
        st.error("❌ **Cannot Display Graph**: Invalid year range")
        st.info("💡 **Please fix**: Start year must be earlier than or equal to end year")
        st.stop()
    
    st.markdown('<h2 class="section-header">📈 Exchange Rate Visualization</h2>', unsafe_allow_html=True)
    
    # Safe date creation (no try-catch needed since we're using selectbox)
    start_date = pd.to_datetime(f"{start_year}-01-01")
    end_date = pd.to_datetime(f"{end_year}-12-31")

    filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    if filtered.empty:
        st.warning("⚠️ **No Data Available**: No exchange rate data found for the selected year range")
        st.info(f"💡 **Available years**: {min_year} to {max_year}")
    else:
        # Original line chart styling
        fig = px.line(
            filtered,
            x='Date',
            y='ExchangeRate',
            title=f"Naira Exchange Rate ({start_year}–{end_year})",
            labels={'ExchangeRate': '₦/USD'},
            template='plotly_dark'
        )
        
        # Original chart styling
        fig.update_traces(
            mode='lines+markers',
            line=dict(width=2),
            marker=dict(size=6),
            hovertemplate='Date: %{x|%Y-%m-%d}<br>Rate: ₦%{y:.2f}'
        )
        
        # Original layout with grid
        fig.update_xaxes(showgrid=True, gridcolor='gray')
        fig.update_yaxes(showgrid=True, gridcolor='gray')
        fig.update_layout(dragmode="pan")
        
        # Display chart in enhanced container
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': True, 
            'displaylogo': False,
            'modeBarButtonsToRemove': ['lasso2d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': f'exchange_rate_{start_year}_{end_year}',
                'height': 600,
                'width': 800,
                'scale': 2
            }
        })
        st.markdown('</div>', unsafe_allow_html=True)

# Enhanced result display for mobile
# Mobile-specific date picker in main body
st.markdown('<h2 class="section-header">📱 Date Checker</h2>', unsafe_allow_html=True)

# Add spacing before the date picker
st.markdown("<br>", unsafe_allow_html=True)

# Use columns for better mobile layout with improved spacing
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<div style='padding: 0.5rem 0;'>", unsafe_allow_html=True)
    specific_date_mobile = st.date_input(
        "📅 Pick a date for rate check",
        value=df["Date"].min(),
        min_value=df["Date"].min(),
        max_value=df["Date"].max(),
        key="specific_date_mobile",
        help="Select a specific date to check the exchange rate"
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div style='padding: 0.5rem 0; text-align: center;'>", unsafe_allow_html=True)
    show_rate_mobile = st.button("🔍 Get Rate", use_container_width=False, key="get_rate_btn")
    st.markdown("</div>", unsafe_allow_html=True)

# Add spacing after the date picker
st.markdown("<br>", unsafe_allow_html=True)

if show_rate_mobile:
    st.markdown('<h2 class="section-header">📌 Exchange Rate Result</h2>', unsafe_allow_html=True)
    
    specific_date_pd = pd.to_datetime(specific_date_mobile)
    exact_row = df[df["Date"] == specific_date_pd]

    if exact_row.empty:
        # Find closest date
        closest = df.iloc[(df["Date"] - specific_date_pd).abs().argsort()[:1]]
        closest_date = closest.iloc[0]['Date'].date()
        closest_rate = closest.iloc[0]['ExchangeRate']
        
        st.info(f"""
        📅 **No data for {specific_date_mobile}**
        
        🎯 **Closest available date:** {closest_date}
        💱 **Rate:** ₦{closest_rate:.2f}/USD
        
        ⏰ **Days difference:** {abs((specific_date_pd - closest.iloc[0]['Date']).days)} days
        """)
    else:
        rate = exact_row.iloc[0]["ExchangeRate"]
        
        # Calculate percentage change from previous day if available
        if len(df) > 1:
            prev_date = specific_date_pd - pd.Timedelta(days=1)
            prev_data = df[df["Date"] == prev_date]
            
            if not prev_data.empty:
                prev_rate = prev_data.iloc[0]["ExchangeRate"]
                pct_change = ((rate - prev_rate) / prev_rate) * 100
                change_emoji = "📈" if pct_change >= 0 else "📉"
                change_color = "#00ff88" if pct_change >= 0 else "#ff6b6b"
                
                st.success(f"""
                🎯 **Exchange Rate Found!**
                
                📅 **Date:** {specific_date_mobile}
                💱 **Rate:** ₦{rate:.2f}/USD
                {change_emoji} **Change:** {pct_change:+.2f}% from previous day
                """)
            else:
                st.success(f"""
                🎯 **Exchange Rate Found!**
                
                📅 **Date:** {specific_date_mobile}
                💱 **Rate:** ₦{rate:.2f}/USD
                """)
        else:
            st.success(f"""
            🎯 **Exchange Rate Found!**
            
            📅 **Date:** {specific_date_mobile}
            💱 **Rate:** ₦{rate:.2f}/USD
            """)

# Footer with enhanced styling
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 2rem; 
            border-radius: 15px; 
            text-align: center;
            margin-top: 3rem;">
    <h3>🇳🇬 Nigerian Exchange Rate Dashboard</h3>
    <p>Data updates automatically from Supabase</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">Last updated: """ + str(df['Date'].max().strftime('%Y-%m-%d')) + """</p>
</div>
""", unsafe_allow_html=True)
