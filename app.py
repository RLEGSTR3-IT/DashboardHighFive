import streamlit as st
from components.layout import setup_page_config, apply_custom_css
from components.sidebar import render_sidebar
from components.viz_piechart import render_piechart_visualization
import pandas as pd

# Force reload module untuk development
import importlib
import sys
if 'components.viz_table' in sys.modules:
    importlib.reload(sys.modules['components.viz_table'])
from components.viz_table import render_table_visualization

# Setup page
setup_page_config()
apply_custom_css()

# Fungsi untuk load data dari Google Sheets
@st.cache_data(ttl=300)
def load_data(data_source):
    """Load data dari Google Sheets berdasarkan DPS/DGS"""
    try:
        # Mapping DPS/DGS ke spreadsheet URL yang berbeda
        sheet_configs = {
            "DPS": "1K-596RSSwJWO1HiAwOBG2gnMSUtrEhvnKIdH8P4w8e4",
            "DGS": "1QazP2uYyoPNZU8qfJuAevHFyJP0SmaSwYSc7JXTchCo"
        }
        
        sheet_id = sheet_configs.get(data_source)
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        
        df = pd.read_csv(csv_url)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Clean NILAI - convert to numeric
        if 'NILAI' in df.columns:
            df['NILAI'] = pd.to_numeric(df['NILAI'], errors='coerce')
        
        # Clean % Results
        if '% Results' in df.columns:
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

# Initialize session state untuk filter data source
if 'data_source' not in st.session_state:
    st.session_state.data_source = "DPS"

# Render sidebar dan dapatkan selected_witel
selected_witel = render_sidebar()

# Header dengan Button Group Filter - HIERARKI H1 BESAR MERAH
col_title, col_spacer, col_filter = st.columns([2, 1, 1])

with col_title:
    st.markdown("""
    <h1 style='margin: 0; color: #ea1d25; font-size: 2.5rem; font-weight: 800; letter-spacing: -0.03em;'>
        Dashboard High Five - RLEGS TR3
    </h1>
    """, unsafe_allow_html=True)

with col_filter:
    # Button Group untuk filter DPS/DGS
    col_dps, col_dgs = st.columns(2)
    
    with col_dps:
        if st.button(
            "DPS",
            key="btn_dps",
            use_container_width=True,
            type="primary" if st.session_state.data_source == "DPS" else "secondary"
        ):
            st.session_state.data_source = "DPS"
            st.rerun()
    
    with col_dgs:
        if st.button(
            "DGS",
            key="btn_dgs",
            use_container_width=True,
            type="primary" if st.session_state.data_source == "DGS" else "secondary"
        ):
            st.session_state.data_source = "DGS"
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Load data berdasarkan filter yang dipilih
with st.spinner(f"⏳ Memuat data {st.session_state.data_source}..."):
    df = load_data(st.session_state.data_source)

if df is not None:
    # Cek apakah witel sudah dipilih
    if selected_witel == "-- Pilih Witel --":
        # Tampilan sebelum filter - REDESIGN LEBIH SUBTLE
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f4f6f8 0%, #e1e7ef 100%); 
                    color: #2d3748; padding: 80px 60px; border-radius: 24px; 
                    text-align: center; 
                    border: 2px solid #cbd5e0;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
                    margin: 40px 0;'>
            <div style='font-size: 64px; margin-bottom: 24px; opacity: 0.4;'>📍</div>
            <h2 style='color: #2d3748; margin: 0 0 16px 0; font-size: 2rem; font-weight: 700;'>
                Pilih WITEL untuk Memulai
            </h2>
            <p style='color: #6b7280; margin: 0; font-size: 1.125rem; font-weight: 500;'>
                Gunakan sidebar di sebelah kiri untuk memilih WITEL yang ingin Anda analisis
            </p>
            <div style='margin-top: 32px;'>
                <div style='display: inline-block; background: white; padding: 12px 28px; 
                            border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
                    <span style='color: #ea1d25; font-size: 0.875rem; font-weight: 700; 
                                letter-spacing: 0.5px;'>
                        👈 PILIH DARI SIDEBAR
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Preview data
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #2d3748; font-size: 1.25rem; font-weight: 700;'>Preview Data</h3>", unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True, height=400)
    else:
        # Filter data berdasarkan witel
        filtered_df = df[df['WITEL'] == selected_witel].copy()
        
        if len(filtered_df) == 0:
            st.warning(f"⚠️ Tidak ada data untuk WITEL: {selected_witel}")
        else:
            # Section 1: Monitoring Produk Witel (Pie Charts)
            render_piechart_visualization(filtered_df, selected_witel)
            
            # Divider
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<hr style='border: 2px solid #e1e7ef; margin: 40px 0;'>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Section 2: Progress Account Manager [WITEL] - MENGGUNAKAN KOMPONEN BARU
            render_table_visualization(filtered_df, selected_witel)

else:
    st.error("❌ Gagal memuat data. Pastikan Google Sheets sudah di-publish sebagai CSV.")

# Footer
st.markdown("<br><br><hr style='border: 1px solid #e1e7ef;'>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center; color: #6b7280; padding: 20px 0;'>
    Dashboard High Five - RLEGS TR3 | Powered by <b style='color: #ea1d25;'>Telkom Indonesia</b> 
    <span style='margin: 0 10px;'>•</span> © 2025
</p>
""", unsafe_allow_html=True)