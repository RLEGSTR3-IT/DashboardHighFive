import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard HighFive Telkom",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Telkom Brand Colors (Merah & Abu)
st.markdown("""
<style>
    /* Main colors: Telkom Red #E60012, Grey #757575 */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    h1 {
        color: #E60012;
        font-weight: 700;
        padding-bottom: 10px;
        border-bottom: 4px solid #E60012;
    }
    
    h2, h3 {
        color: #757575;
        font-weight: 600;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        color: #E60012;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 600;
        color: #757575;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #E60012 0%, #C4000F 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #E60012;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #C4000F;
        box-shadow: 0 4px 12px rgba(230, 0, 18, 0.3);
    }
    
    /* Selectbox styling */
    .stSelectbox label {
        color: white !important;
        font-weight: 600;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #E60012;
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #E60012 0%, #C4000F 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    /* DataFrame styling */
    .dataframe {
        border: 2px solid #E60012 !important;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Fungsi untuk load data
@st.cache_data(ttl=300)
def load_data(url):
    """Load data dari Google Sheets"""
    try:
        if '/edit' in url:
            sheet_id = url.split('/d/')[1].split('/')[0]
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        else:
            csv_url = url
        
        df = pd.read_csv(csv_url)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Convert % columns to numeric
        if '% Results' in df.columns:
            df['% Results'] = pd.to_numeric(df['% Results'], errors='coerce')
        if '% Progress' in df.columns:
            df['% Progress'] = pd.to_numeric(df['% Progress'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Fungsi untuk calculate win/lose
def calculate_win_lose(filtered_df):
    """Calculate average % Results untuk Astinet Bundling DDoS"""
    astinet_data = filtered_df[filtered_df['PRODUCT HIGH FIVE'] == 'Astinet Bundling DDoS']
    
    if len(astinet_data) > 0:
        avg_result = astinet_data['% Results'].mean()
        win_rate = avg_result
        lose_rate = 100 - avg_result
        return win_rate, lose_rate, len(astinet_data)
    else:
        return 0, 0, 0

# URL Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1QazP2uYyoPNZU8qfJuAevHFyJP0SmaSwYSc7JXTchCo/edit?usp=sharing"

# List Witel
WITEL_LIST = [
    "JATIM BARAT",
    "YOGYA JATENG SELATAN",
    "SEMARANG JATENG UTARA",
    "SURAMADU",
    "BALI",
    "NUSA TENGGARA",
    "JATIM TIMUR",
    "SOLO JATENG TIMUR"
]

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("<h2 style='color: white; text-align: center;'>⚙️ FILTER DATA</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
    
    # Filter Witel
    selected_witel = st.selectbox(
        "📍 PILIH WITEL",
        options=["-- Pilih Witel --"] + WITEL_LIST,
        key="witel_filter"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Refresh button
    if st.button("🔄 REFRESH DATA", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='color: white; font-size: 12px; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;'>
        <b>ℹ️ CARA PENGGUNAAN:</b><br>
        1. Pilih WITEL dari dropdown<br>
        2. Visualisasi akan muncul otomatis<br>
        3. Data di-refresh setiap 5 menit
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p style='color: white; text-align: center; font-size: 10px;'>© 2024 Telkom Indonesia</p>", unsafe_allow_html=True)

# ========== MAIN CONTENT ==========

# Header
st.markdown("<h1>🚀 DASHBOARD MONITORING HIGH FIVE</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #757575; font-size: 16px;'>Monitor performa <b>Astinet Bundling DDoS</b> secara real-time</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Load data
with st.spinner("⏳ Memuat data..."):
    df = load_data(SHEET_URL)

if df is not None:
    # Cek apakah witel sudah dipilih
    if selected_witel == "-- Pilih Witel --":
        # Tampilan sebelum filter
        st.markdown("""
        <div class='info-box'>
            <h3 style='color: white; margin: 0;'>👈 Silakan Pilih WITEL</h3>
            <p style='color: white; margin: 5px 0 0 0;'>Pilih WITEL dari sidebar untuk menampilkan visualisasi data</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Preview data
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3>📊 Preview Data</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📋 Total Records", len(df))
        with col2:
            total_witel = df['WITEL'].nunique() if 'WITEL' in df.columns else 0
            st.metric("📍 Total WITEL", total_witel)
        with col3:
            total_products = df['PRODUCT HIGH FIVE'].nunique() if 'PRODUCT HIGH FIVE' in df.columns else 0
            st.metric("📦 Total Products", total_products)
        
        st.dataframe(df.head(10), use_container_width=True, height=300)
        
    else:
        # Filter data berdasarkan witel
        filtered_df = df[df['WITEL'] == selected_witel].copy()
        
        if len(filtered_df) == 0:
            st.warning(f"⚠️ Tidak ada data untuk WITEL: {selected_witel}")
        else:
            # Calculate metrics
            win_rate, lose_rate, total_records = calculate_win_lose(filtered_df)
            
            # Metrics Row
            st.markdown(f"<h2>📍 {selected_witel}</h2>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📊 Total Data", len(filtered_df))
            
            with col2:
                st.metric("🎯 Astinet Bundling DDoS", total_records)
            
            with col3:
                st.metric("✅ WIN RATE", f"{win_rate:.1f}%")
            
            with col4:
                st.metric("❌ LOSE RATE", f"{lose_rate:.1f}%")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # ========== VISUALISASI ==========
            
            if total_records > 0:
                # Create two columns for charts
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("<h3>📊 Win vs Lose Rate</h3>", unsafe_allow_html=True)
                    
                    # Pie Chart - Win/Lose
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=['WIN', 'LOSE'],
                        values=[win_rate, lose_rate],
                        hole=0.5,
                        marker=dict(
                            colors=['#E60012', '#757575'],
                            line=dict(color='white', width=2)
                        ),
                        textinfo='label+percent',
                        textfont=dict(size=16, color='white', family='Arial Black'),
                        hovertemplate='<b>%{label}</b><br>%{value:.1f}%<extra></extra>'
                    )])
                    
                    fig_pie.update_layout(
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.2,
                            xanchor="center",
                            x=0.5,
                            font=dict(size=14, color='#757575')
                        ),
                        height=400,
                        margin=dict(t=20, b=20, l=20, r=20),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        annotations=[dict(
                            text=f'<b>{win_rate:.1f}%</b><br>WIN',
                            x=0.5, y=0.5,
                            font=dict(size=24, color='#E60012', family='Arial Black'),
                            showarrow=False
                        )]
                    )
                    
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col2:
                    st.markdown("<h3>📈 Performance Gauge</h3>", unsafe_allow_html=True)
                    
                    # Gauge Chart
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=win_rate,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "<b>WIN RATE</b>", 'font': {'size': 24, 'color': '#757575'}},
                        delta={'reference': 50, 'increasing': {'color': "#E60012"}},
                        number={'suffix': "%", 'font': {'size': 48, 'color': '#E60012'}},
                        gauge={
                            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#757575"},
                            'bar': {'color': "#E60012", 'thickness': 0.8},
                            'bgcolor': "white",
                            'borderwidth': 2,
                            'bordercolor': "#757575",
                            'steps': [
                                {'range': [0, 33], 'color': '#ffcccc'},
                                {'range': [33, 66], 'color': '#ff9999'},
                                {'range': [66, 100], 'color': '#ff6666'}
                            ],
                            'threshold': {
                                'line': {'color': "#333", 'width': 4},
                                'thickness': 0.75,
                                'value': 80
                            }
                        }
                    ))
                    
                    fig_gauge.update_layout(
                        height=400,
                        margin=dict(t=80, b=20, l=20, r=20),
                        paper_bgcolor='rgba(0,0,0,0)',
                        font={'family': "Arial"}
                    )
                    
                    st.plotly_chart(fig_gauge, use_container_width=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Detail table
                st.markdown("<h3>📋 Detail Astinet Bundling DDoS</h3>", unsafe_allow_html=True)
                
                astinet_detail = filtered_df[filtered_df['PRODUCT HIGH FIVE'] == 'Astinet Bundling DDoS'][
                    ['CUSTOMER_NAME', 'AM', 'NILAI', '% Progress', '% Results', 'Result']
                ].sort_values('% Results', ascending=False)
                
                st.dataframe(
                    astinet_detail,
                    use_container_width=True,
                    height=400,
                    column_config={
                        "% Progress": st.column_config.ProgressColumn(
                            "Progress",
                            format="%.1f%%",
                            min_value=0,
                            max_value=100,
                        ),
                        "% Results": st.column_config.ProgressColumn(
                            "Results",
                            format="%.1f%%",
                            min_value=0,
                            max_value=100,
                        ),
                    }
                )
                
                # Download button
                csv = astinet_detail.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Data CSV",
                    data=csv,
                    file_name=f"astinet_bundling_{selected_witel.lower().replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
            else:
                st.info(f"ℹ️ Tidak ada data **Astinet Bundling DDoS** untuk WITEL {selected_witel}")
                
                # Tampilkan semua data witel tersebut
                st.markdown("<h3>📋 Semua Data di WITEL ini</h3>", unsafe_allow_html=True)
                st.dataframe(filtered_df, use_container_width=True, height=400)

else:
    st.error("❌ Gagal memuat data. Pastikan Google Sheets sudah di-publish sebagai CSV.")

# Footer
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #757575;'>Dashboard Monitoring High Five | Powered by <b style='color: #E60012;'>Telkom Indonesia</b></p>", unsafe_allow_html=True)