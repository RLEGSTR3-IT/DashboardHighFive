import streamlit as st
import pandas as pd

def render_table_visualization(df, selected_witel):
    """
    Render section Progress Account Manager untuk WITEL tertentu
    """
    
    # Section Header dengan nama WITEL
    st.markdown(f"""
    <div class='dashboard-card' style='background: white; padding: 28px 32px; border-radius: 20px; 
                box-shadow: 0 1px 3px 0 rgba(16, 24, 40, 0.04); border: 1px solid #e1e7ef; margin-bottom: 32px;'>
        <h2 style='color: #6b7280; margin: 0; font-size: 1.5rem; font-weight: 700; letter-spacing: -0.02em;'>
            📋 Progress Account Manager {selected_witel}
        </h2>
        <p style='color: #9ca3af; margin: 8px 0 0 0; font-size: 0.875rem; font-weight: 500;'>
            Detail progress produk per Account Manager (Coming Soon)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Placeholder content
    st.markdown("""
    <div style='background: white; padding: 60px 40px; border-radius: 16px; 
                box-shadow: 0 1px 3px 0 rgba(16, 24, 40, 0.04); border: 1px solid #e1e7ef; 
                text-align: center;'>
        <div style='font-size: 4rem; margin-bottom: 24px; opacity: 0.3;'>📊</div>
        <h3 style='color: #6b7280; margin: 0 0 12px 0; font-size: 1.25rem; font-weight: 700;'>
            Visualisasi Tabel Segera Hadir
        </h3>
        <p style='color: #9ca3af; margin: 0; font-size: 0.9375rem; max-width: 500px; margin: 0 auto;'>
            Section ini akan menampilkan detail progress produk per Account Manager dalam format tabel interaktif. 
            Silakan tunggu spesifikasi lebih lanjut untuk implementasi lengkap.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Preview data metrics
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_rows = len(df)
        st.markdown(f"""
        <div style='background: #f4f6f8; padding: 20px; border-radius: 12px; text-align: center;'>
            <div style='color: #9ca3af; font-size: 0.7rem; font-weight: 600; 
                       text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>
                Total Rows
            </div>
            <div style='color: #6b7280; font-size: 1.5rem; font-weight: 700;'>
                {total_rows}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_am = df['AM'].nunique() if 'AM' in df.columns else 0
        st.markdown(f"""
        <div style='background: #f4f6f8; padding: 20px; border-radius: 12px; text-align: center;'>
            <div style='color: #9ca3af; font-size: 0.7rem; font-weight: 600; 
                       text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>
                Total AM
            </div>
            <div style='color: #6b7280; font-size: 1.5rem; font-weight: 700;'>
                {total_am}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_products = df['PRODUCT'].nunique() if 'PRODUCT' in df.columns else 0
        st.markdown(f"""
        <div style='background: #f4f6f8; padding: 20px; border-radius: 12px; text-align: center;'>
            <div style='color: #9ca3af; font-size: 0.7rem; font-weight: 600; 
                       text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>
                Unique Products
            </div>
            <div style='color: #6b7280; font-size: 1.5rem; font-weight: 700;'>
                {total_products}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_progress = df['% Progress'].mean() if '% Progress' in df.columns else 0
        st.markdown(f"""
        <div style='background: #f4f6f8; padding: 20px; border-radius: 12px; text-align: center;'>
            <div style='color: #9ca3af; font-size: 0.7rem; font-weight: 600; 
                       text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>
                Avg Progress
            </div>
            <div style='color: #6b7280; font-size: 1.5rem; font-weight: 700;'>
                {avg_progress:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Optional: Preview raw data dalam expander
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔍 Preview Data Mentah"):
        st.dataframe(df, use_container_width=True, height=400)