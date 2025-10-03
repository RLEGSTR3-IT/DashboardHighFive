import streamlit as st
from components.layout import setup_page_config, apply_custom_css
from components.sidebar import render_sidebar
from components.viz_astinet import render_astinet_visualization
from components.viz_other import render_other_visualization
import pandas as pd

# Setup page
setup_page_config()
apply_custom_css()

# Fungsi untuk load data
@st.cache_data(ttl=300)
def load_data(url):
    """Load data dari Google Sheets dan clean data"""
    try:
        if '/edit' in url:
            sheet_id = url.split('/d/')[1].split('/')[0]
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        else:
            csv_url = url
        
        df = pd.read_csv(csv_url)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Clean NILAI - convert to numeric
        if 'NILAI' in df.columns:
            df['NILAI'] = pd.to_numeric(df['NILAI'], errors='coerce')
        
        # Clean % Results - PERBAIKAN UTAMA DI SINI
        if '% Results' in df.columns:
            # Hapus karakter % dan konversi ke numeric
            df['% Results'] = df['% Results'].astype(str).str.replace('%', '').str.strip()
            df['% Results'] = pd.to_numeric(df['% Results'], errors='coerce')
        
        # Clean % Progress
        if '% Progress' in df.columns:
            df['% Progress'] = df['% Progress'].astype(str).str.replace('%', '').str.strip()
            df['% Progress'] = pd.to_numeric(df['% Progress'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# URL Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1QazP2uYyoPNZU8qfJuAevHFyJP0SmaSwYSc7JXTchCo/edit?usp=sharing"

# Load data
with st.spinner("⏳ Memuat data..."):
    df = load_data(SHEET_URL)

if df is not None:
    # Render sidebar dan dapatkan filter
    selected_witel = render_sidebar()
    
    # Header
    st.markdown("<h1 style='text-align: center;'>🚀 DASHBOARD MONITORING HIGH FIVE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #757575; font-size: 18px; margin-bottom: 40px;'>Monitor performa <b>Astinet Bundling DDoS</b> secara real-time</p>", unsafe_allow_html=True)
    
    # Cek apakah witel sudah dipilih
    if selected_witel == "-- Pilih Witel --":
        # Tampilan sebelum filter
        st.markdown("""
        <div style='background: linear-gradient(135deg, #E60012 0%, #C4000F 100%); 
                    color: white; padding: 60px 40px; border-radius: 20px; 
                    text-align: center; box-shadow: 0 8px 32px rgba(230, 0, 18, 0.3);
                    margin: 40px 0;'>
            <h2 style='color: white; margin: 0; font-size: 32px;'>👈 Silakan Pilih WITEL</h2>
            <p style='color: white; margin: 20px 0 0 0; font-size: 18px; opacity: 0.95;'>
                Pilih WITEL dari sidebar untuk menampilkan visualisasi data
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Preview data dengan card design
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div style='background: white; padding: 30px; border-radius: 16px; 
                        box-shadow: 0 4px 16px rgba(0,0,0,0.08); border-left: 6px solid #E60012;'>
                <div style='color: #757575; font-size: 14px; font-weight: 600; margin-bottom: 10px;'>
                    📋 TOTAL RECORDS
                </div>
                <div style='color: #E60012; font-size: 42px; font-weight: 700;'>
                    """ + str(len(df)) + """
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_witel = df['WITEL'].nunique() if 'WITEL' in df.columns else 0
            st.markdown("""
            <div style='background: white; padding: 30px; border-radius: 16px; 
                        box-shadow: 0 4px 16px rgba(0,0,0,0.08); border-left: 6px solid #757575;'>
                <div style='color: #757575; font-size: 14px; font-weight: 600; margin-bottom: 10px;'>
                    📍 TOTAL WITEL
                </div>
                <div style='color: #757575; font-size: 42px; font-weight: 700;'>
                    """ + str(total_witel) + """
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_products = df['PRODUCT HIGH FIVE'].nunique() if 'PRODUCT HIGH FIVE' in df.columns else 0
            st.markdown("""
            <div style='background: white; padding: 30px; border-radius: 16px; 
                        box-shadow: 0 4px 16px rgba(0,0,0,0.08); border-left: 6px solid #E60012;'>
                <div style='color: #757575; font-size: 14px; font-weight: 600; margin-bottom: 10px;'>
                    📦 TOTAL PRODUCTS
                </div>
                <div style='color: #E60012; font-size: 42px; font-weight: 700;'>
                    """ + str(total_products) + """
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #757575;'>📊 Preview Data</h3>", unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True, height=400)
        
    else:
        # Filter data berdasarkan witel
        filtered_df = df[df['WITEL'] == selected_witel].copy()
        
        if len(filtered_df) == 0:
            st.warning(f"⚠️ Tidak ada data untuk WITEL: {selected_witel}")
        else:
            # BAGIAN ATAS: Visualisasi Astinet Bundling DDoS
            render_astinet_visualization(filtered_df, selected_witel)
            
            # Divider
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<hr style='border: 2px solid #E6E6E6; margin: 40px 0;'>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # BAGIAN BAWAH: Visualisasi Lainnya (extensible)
            render_other_visualization(filtered_df, selected_witel)

else:
    st.error("❌ Gagal memuat data. Pastikan Google Sheets sudah di-publish sebagai CSV.")

# Footer
st.markdown("<br><br><hr style='border: 1px solid #E6E6E6;'>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center; color: #757575; padding: 20px 0;'>
    Dashboard Monitoring High Five | Powered by <b style='color: #E60012;'>Telkom Indonesia</b> 
    <span style='margin: 0 10px;'>•</span> © 2024
</p>
""", unsafe_allow_html=True)