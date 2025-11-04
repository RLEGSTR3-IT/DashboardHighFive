import streamlit as st
from components.layout import setup_page_config, apply_custom_css
from components.sidebar import render_sidebar
from components.viz_piechart import render_piechart_visualization
from components.viz_table import render_table_visualization
import pandas as pd

# Force reload modules untuk development
import importlib
import sys

# Reload modules jika ada perubahan
modules_to_reload = ['components.layout', 'components.sidebar', 'components.viz_piechart', 'components.viz_table']
for module_name in modules_to_reload:
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])

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

# Initialize session state untuk view mode (digunakan di viz_table)
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'card'

# Render sidebar dan dapatkan selected_witel
selected_witel = render_sidebar()

# Header dengan Button Group Filter
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
        # Tampilan sebelum filter
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%); 
                    color: #2d3748; padding: 80px 60px; border-radius: 24px; 
                    text-align: center; 
                    border: 2px solid #e5e7eb;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
                    margin: 40px 0;'>
            <div style='font-size: 64px; margin-bottom: 24px; opacity: 0.5;'>📍</div>
            <h2 style='color: #1a202c; margin: 0 0 16px 0; font-size: 2rem; font-weight: 800;'>
                Pilih WITEL untuk Memulai
            </h2>
            <p style='color: #6b7280; margin: 0; font-size: 1.125rem; font-weight: 500;'>
                Gunakan sidebar di sebelah kiri untuk memilih WITEL yang ingin Anda analisis
            </p>
            <div style='margin-top: 32px;'>
                <div style='display: inline-block; background: linear-gradient(135deg, #ea1d25 0%, #d61921 100%); 
                            padding: 12px 28px; border-radius: 12px; 
                            box-shadow: 0 4px 16px rgba(234, 29, 37, 0.3);'>
                    <span style='color: white; font-size: 0.875rem; font-weight: 700; 
                                letter-spacing: 0.5px;'>
                        👈 PILIH DARI SIDEBAR
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Preview data dengan styling modern
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%); 
                    padding: 24px 28px; border-radius: 20px; 
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); 
                    border: 1px solid #e5e7eb; margin-bottom: 20px;'>
            <div style='display: flex; align-items: center; gap: 16px;'>
                <div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                            width: 48px; height: 48px; border-radius: 12px;
                            display: flex; align-items: center; justify-content: center;'>
                    <span style='font-size: 24px;'>👁️</span>
                </div>
                <div>
                    <h3 style='color: #1a202c; margin: 0; font-size: 1.25rem; font-weight: 900;'>
                        Preview Data
                    </h3>
                    <p style='color: #6b7280; margin: 4px 0 0 0; font-size: 0.875rem; font-weight: 500;'>
                        Tampilan 10 baris pertama dari data {st.session_state.data_source}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(df.head(10), use_container_width=True, height=400)
    else:
        # Filter data berdasarkan witel
        filtered_df = df[df['WITEL'] == selected_witel].copy()
        
        if len(filtered_df) == 0:
            # Warning dengan styling modern
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                        padding: 24px 28px; border-radius: 16px; 
                        border: 2px solid #fbbf24;
                        box-shadow: 0 4px 16px rgba(251, 191, 36, 0.2);
                        margin: 20px 0;'>
                <div style='display: flex; align-items: center; gap: 16px;'>
                    <div style='background: #fbbf24; width: 48px; height: 48px; 
                                border-radius: 12px; display: flex; align-items: center; 
                                justify-content: center;'>
                        <span style='font-size: 24px;'>⚠️</span>
                    </div>
                    <div>
                        <div style='color: #78350f; font-weight: 800; font-size: 1.125rem; 
                                   margin-bottom: 4px;'>
                            Tidak Ada Data
                        </div>
                        <div style='color: #92400e; font-size: 0.875rem; font-weight: 600;'>
                            Tidak ada data untuk WITEL: <b>{selected_witel}</b>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Section 1: Monitoring Produk Witel (Pie Charts)
            render_piechart_visualization(filtered_df, selected_witel)
            
            # Divider dengan styling modern
            st.markdown("""
            <div style='margin: 60px 0 40px 0;'>
                <div style='height: 2px; background: linear-gradient(90deg, transparent 0%, #e5e7eb 20%, #e5e7eb 80%, transparent 100%);'></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Section 2: Progress Account Manager
            render_table_visualization(filtered_df, selected_witel)

else:
    # Error dengan styling modern
    st.markdown("""
    <div style='background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); 
                padding: 24px 28px; border-radius: 16px; 
                border: 2px solid #ef4444;
                box-shadow: 0 4px 16px rgba(239, 68, 68, 0.2);
                margin: 20px 0;'>
        <div style='display: flex; align-items: center; gap: 16px;'>
            <div style='background: #ef4444; width: 48px; height: 48px; 
                        border-radius: 12px; display: flex; align-items: center; 
                        justify-content: center;'>
                <span style='font-size: 24px;'>❌</span>
            </div>
            <div>
                <div style='color: #7f1d1d; font-weight: 800; font-size: 1.125rem; 
                           margin-bottom: 4px;'>
                    Gagal Memuat Data
                </div>
                <div style='color: #991b1b; font-size: 0.875rem; font-weight: 600;'>
                    Pastikan Google Sheets sudah di-publish sebagai CSV dan dapat diakses publik
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer dengan styling modern
st.markdown("""
<div style='margin-top: 80px;'>
    <div style='height: 1px; background: linear-gradient(90deg, transparent 0%, #e5e7eb 20%, #e5e7eb 80%, transparent 100%); margin-bottom: 32px;'></div>
    <div style='text-align: center; padding: 20px 0;'>
        <div style='color: #1a202c; font-weight: 700; font-size: 0.875rem; margin-bottom: 8px;'>
            Dashboard High Five - RLEGS TR3
        </div>
        <div style='color: #6b7280; font-size: 0.8rem; font-weight: 500;'>
            Powered by <span style='color: #ea1d25; font-weight: 700;'>Telkom Indonesia</span> 
            <span style='margin: 0 8px; color: #e5e7eb;'>•</span> 
            © 2025
        </div>
    </div>
</div>
""", unsafe_allow_html=True)