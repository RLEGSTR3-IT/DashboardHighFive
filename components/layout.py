import streamlit as st

def setup_page_config():
    """Setup konfigurasi halaman Streamlit"""
    st.set_page_config(
        page_title="HIGH FIVE - RLEGS TR3",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    """Apply custom CSS sesuai overview.css dengan Telkom brand"""
    st.markdown("""
    <style>
        /* Import Google Fonts - Inter */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        /* ===== ROOT VARIABLES ===== */
        :root {
            --telkom-red: #ea1d25;
            --telkom-red-dark: #c41e24;
            --telkom-red-subtle: rgba(234, 29, 37, 0.06);
            
            --white: #ffffff;
            --gray-50: #FAFAFA;
            --gray-100: #f5f5f5;
            --gray-200: #e5e7eb;
            --gray-300: #d1d5db;
            --gray-400: #9ca3af;
            --gray-500: #6b7280;
            --gray-600: #4a5568;
            --gray-700: #2d3748;
            --gray-800: #1a202c;
            --gray-900: #171923;
            
            --shadow-xs: 0 1px 2px 0 rgba(16, 24, 40, 0.04);
            --shadow-sm: 0 1px 3px 0 rgba(16, 24, 40, 0.06), 0 1px 2px -1px rgba(16, 24, 40, 0.06);
            --shadow-card: 0 1px 3px 0 rgba(16, 24, 40, 0.04), 0 1px 2px -1px rgba(16, 24, 40, 0.04);
            --shadow-card-hover: 0 4px 16px -2px rgba(16, 24, 40, 0.08), 0 2px 8px -2px rgba(16, 24, 40, 0.04);
            
            --gradient-red: linear-gradient(135deg, var(--telkom-red) 0%, #d61921 100%);
            
            --radius-lg: 12px;
            --radius-xl: 16px;
            --radius-2xl: 20px;
            
            --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            
            --font-sans: "Inter", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial;
        }
        
        /* ===== GLOBAL STYLES ===== */
        * {
            font-family: var(--font-sans);
        }
        
        .main {
            background: #FAFAFA !important;
            padding: 16px 32px !important;
        }
        
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
        }
        
        /* ===== SIDEBAR STYLING - SOLID COLOR ===== */
        [data-testid="stSidebar"] {
            background: #ea1d25 !important;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.1);
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: white;
        }
        
        [data-testid="stSidebar"] label {
            color: white !important;
            font-weight: 600;
        }
        
        [data-testid="stSidebar"] .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.15);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            color: white;
            font-weight: 600;
            backdrop-filter: blur(10px);
        }
        
        [data-testid="stSidebar"] .stSelectbox > div > div:hover {
            border-color: rgba(255, 255, 255, 0.5);
            background: rgba(255, 255, 255, 0.2);
        }
        
        /* ===== SIDEBAR COLLAPSE BUTTON - WHITE ICON ===== */
        [data-testid="collapsedControl"] {
            color: white !important;
        }
        
        [data-testid="collapsedControl"] svg {
            fill: white !important;
            stroke: white !important;
        }
        
        button[kind="header"] {
            color: white !important;
        }
        
        button[kind="header"] svg {
            fill: white !important;
        }
        
        /* Minimize icon di sidebar */
        [data-testid="stSidebar"] button[kind="header"] {
            color: white !important;
        }
        
        [data-testid="stSidebar"] button[kind="header"] svg {
            fill: white !important;
            stroke: white !important;
        }
        
        /* ===== TYPOGRAPHY ===== */
        h1 {
            color: var(--gray-900);
            font-weight: 700;
            letter-spacing: -0.02em;
            line-height: 1.2;
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        h2 {
            color: var(--telkom-red);
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        h3 {
            color: var(--gray-700);
            font-weight: 600;
        }
        
        /* ===== BUTTONS ===== */
        .stButton>button {
            border-radius: var(--radius-lg);
            font-weight: 600;
            font-size: 0.875rem;
            transition: var(--transition);
            box-shadow: var(--shadow-xs);
        }
        
        .stButton>button[kind="primary"] {
            background: var(--gradient-red);
            color: white;
            border: 1px solid var(--telkom-red);
        }
        
        .stButton>button[kind="primary"]:hover {
            background: linear-gradient(135deg, var(--telkom-red-dark) 0%, #a01419 100%);
            transform: translateY(-1px);
            box-shadow: var(--shadow-sm);
        }
        
        .stButton>button[kind="secondary"] {
            background: var(--white);
            color: var(--gray-700);
            border: 1px solid var(--gray-300);
        }
        
        .stButton>button[kind="secondary"]:hover {
            background: var(--gray-50);
            border-color: var(--gray-400);
        }
        
        [data-testid="stSidebar"] .stButton>button {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
        }
        
        [data-testid="stSidebar"] .stButton>button:hover {
            background: rgba(255, 255, 255, 0.25);
            border-color: rgba(255, 255, 255, 0.5);
        }
        
        /* ===== CARDS ===== */
        .dashboard-card {
            background: var(--white);
            border-radius: var(--radius-2xl);
            box-shadow: var(--shadow-card);
            border: 1px solid var(--gray-200);
            transition: var(--transition);
        }
        
        .dashboard-card:hover {
            box-shadow: var(--shadow-card-hover);
            border-color: var(--gray-300);
        }
        
        /* ===== PLOTLY CHARTS ===== */
        .js-plotly-plot {
            border-radius: var(--radius-xl);
            overflow: hidden;
        }
        
        /* ===== DATAFRAME ===== */
        .dataframe {
            border: none !important;
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-card);
        }
        
        .dataframe thead tr th {
            background: var(--gradient-red) !important;
            color: white !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            padding: 16px !important;
        }
        
        .dataframe tbody tr:nth-child(even) {
            background: var(--gray-50) !important;
        }
        
        .dataframe tbody tr:hover {
            background: var(--telkom-red-subtle) !important;
        }
        
        /* ===== SPINNER ===== */
        .stSpinner > div {
            border-top-color: var(--telkom-red) !important;
        }
        
        /* ===== HIDE STREAMLIT BRANDING ===== */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* ===== ANIMATIONS ===== */
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .dashboard-card {
            animation: slideUp 0.4s ease-out;
        }
        
        /* ===== CUSTOM EXPANDER STYLING ===== */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #ea1d25 0%, #d61921 100%) !important;
            color: white !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 16px 20px !important;
            border: none !important;
        }
        
        .streamlit-expanderHeader:hover {
            background: linear-gradient(135deg, #d61921 0%, #c41e24 100%) !important;
        }
        
        .streamlit-expanderContent {
            border: 1px solid #e5e7eb !important;
            border-top: none !important;
            border-radius: 0 0 12px 12px !important;
            background: white !important;
        }
    </style>
    """, unsafe_allow_html=True)