import streamlit as st

def setup_page_config():
    """Setup konfigurasi halaman Streamlit"""
    st.set_page_config(
        page_title="Dashboard HighFive Telkom",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    """Apply custom CSS untuk styling Telkom brand"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        
        /* Global Styles */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .main {
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        }
        
        /* Header styling dengan gradient */
        h1 {
            background: linear-gradient(135deg, #E60012 0%, #C4000F 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            letter-spacing: -0.5px;
            padding-bottom: 20px;
        }
        
        h2 {
            color: #E60012;
            font-weight: 700;
            letter-spacing: -0.3px;
        }
        
        h3 {
            color: #757575;
            font-weight: 600;
            margin-bottom: 20px;
        }
        
        /* Metrics styling dengan modern card */
        [data-testid="stMetricValue"] {
            font-size: 36px;
            font-weight: 800;
            color: #E60012;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 13px;
            font-weight: 600;
            color: #757575;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Sidebar styling dengan gradient modern */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #E60012 0%, #B8000E 50%, #8A000A 100%);
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.1);
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: white;
        }
        
        [data-testid="stSidebar"] label {
            color: white !important;
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Button styling dengan hover effect */
        .stButton>button {
            background: linear-gradient(135deg, #E60012 0%, #C4000F 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 14px 28px;
            font-weight: 700;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 16px rgba(230, 0, 18, 0.3);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(230, 0, 18, 0.4);
            background: linear-gradient(135deg, #FF0015 0%, #D40011 100%);
        }
        
        .stButton>button:active {
            transform: translateY(0px);
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.15);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            color: white;
            font-weight: 600;
            backdrop-filter: blur(10px);
        }
        
        .stSelectbox > div > div:hover {
            border-color: rgba(255, 255, 255, 0.5);
            background: rgba(255, 255, 255, 0.2);
        }
        
        /* DataFrame styling modern */
        .dataframe {
            border: none !important;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        
        .dataframe thead tr th {
            background: linear-gradient(135deg, #E60012 0%, #C4000F 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
            padding: 16px !important;
            border: none !important;
        }
        
        .dataframe tbody tr:nth-child(even) {
            background: #f8f9fa !important;
        }
        
        .dataframe tbody tr:hover {
            background: #fff5f5 !important;
            transition: background 0.2s ease;
        }
        
        /* Card container */
        .metric-card {
            background: white;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border-left: 6px solid #E60012;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        }
        
        /* Info box dengan glassmorphism */
        .info-box {
            background: linear-gradient(135deg, rgba(230, 0, 18, 0.95) 0%, rgba(196, 0, 15, 0.95) 100%);
            backdrop-filter: blur(10px);
            color: white;
            padding: 32px;
            border-radius: 20px;
            margin: 20px 0;
            box-shadow: 0 8px 32px rgba(230, 0, 18, 0.3);
        }
        
        /* Plotly chart container */
        .js-plotly-plot {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        
        /* Spinner custom */
        .stSpinner > div {
            border-top-color: #E60012 !important;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: white;
            border-radius: 12px 12px 0 0;
            padding: 12px 24px;
            font-weight: 600;
            color: #757575;
            border: 2px solid transparent;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #E60012 0%, #C4000F 100%);
            color: white;
            border-color: #E60012;
        }
        
        /* Progress bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #E60012 0%, #FF4444 100%);
            border-radius: 8px;
        }
        
        /* Hide default streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            h1 {
                font-size: 28px;
            }
            
            [data-testid="stMetricValue"] {
                font-size: 24px;
            }
        }
    </style>
    """, unsafe_allow_html=True)