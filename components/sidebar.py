import streamlit as st

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

def render_sidebar():
    """Render sidebar dengan filter WITEL"""
    
    with st.sidebar:
        # Logo/Header section
        st.markdown("""
        <div style='text-align: center; padding: 20px 0 30px 0;'>
            <h1 style='color: white; font-size: 28px; margin: 0; font-weight: 800; 
                       letter-spacing: -0.5px; text-shadow: 2px 2px 8px rgba(0,0,0,0.2);'>
                🚀 HIGH FIVE
            </h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 13px; margin: 8px 0 0 0; 
                      font-weight: 600; letter-spacing: 1px;'>
                MONITORING DASHBOARD
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='border-top: 2px solid rgba(255,255,255,0.3); 
                    margin: 0 -20px 30px -20px;'></div>
        """, unsafe_allow_html=True)
        
        # Filter Section Header
        st.markdown("""
        <div style='background: rgba(255,255,255,0.15); padding: 16px; 
                    border-radius: 12px; margin-bottom: 24px; backdrop-filter: blur(10px);'>
            <h3 style='color: white; margin: 0; font-size: 16px; font-weight: 700;
                       letter-spacing: 0.5px; text-transform: uppercase;'>
                ⚙️ FILTER DATA
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Filter Witel
        st.markdown("""
        <p style='color: white; font-size: 13px; font-weight: 600; 
                  margin-bottom: 8px; letter-spacing: 0.5px;'>
            📍 PILIH WITEL
        </p>
        """, unsafe_allow_html=True)
        
        selected_witel = st.selectbox(
            "witel_select",
            options=["-- Pilih Witel --"] + WITEL_LIST,
            key="witel_filter",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Refresh button dengan icon
        if st.button("🔄  REFRESH DATA", use_container_width=True, key="refresh_btn"):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Divider
        st.markdown("""
        <div style='border-top: 2px solid rgba(255,255,255,0.3); 
                    margin: 30px -20px;'></div>
        """, unsafe_allow_html=True)
        
        # Info section dengan card design
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 20px; 
                    border-radius: 12px; backdrop-filter: blur(10px);
                    border: 2px solid rgba(255,255,255,0.2);'>
            <div style='display: flex; align-items: center; margin-bottom: 12px;'>
                <span style='font-size: 24px; margin-right: 12px;'>💡</span>
                <span style='color: white; font-size: 14px; font-weight: 700; 
                             letter-spacing: 0.5px;'>CARA PENGGUNAAN</span>
            </div>
            <div style='color: rgba(255,255,255,0.95); font-size: 13px; 
                        line-height: 1.8; margin-left: 36px;'>
                <div style='margin-bottom: 8px;'>
                    <span style='color: white; font-weight: 700;'>1.</span> 
                    Pilih WITEL dari dropdown
                </div>
                <div style='margin-bottom: 8px;'>
                    <span style='color: white; font-weight: 700;'>2.</span> 
                    Visualisasi muncul otomatis
                </div>
                <div style='margin-bottom: 8px;'>
                    <span style='color: white; font-weight: 700;'>3.</span> 
                    Data refresh setiap 5 menit
                </div>
                <div>
                    <span style='color: white; font-weight: 700;'>4.</span> 
                    Download data tersedia
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Status indicator
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background: rgba(76, 175, 80, 0.2); padding: 12px; 
                    border-radius: 8px; border-left: 4px solid #4CAF50;'>
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 20px; margin-right: 10px;'>●</span>
                <span style='color: white; font-size: 12px; font-weight: 600;'>
                    SYSTEM STATUS: ONLINE
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; padding-top: 20px; 
                    border-top: 2px solid rgba(255,255,255,0.2);'>
            <p style='color: rgba(255,255,255,0.7); font-size: 11px; 
                      margin: 0; letter-spacing: 0.5px;'>
                © 2024 Telkom Indonesia
            </p>
            <p style='color: rgba(255,255,255,0.5); font-size: 10px; 
                      margin: 4px 0 0 0;'>
                v1.0.0 • Dashboard HighFive
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    return selected_witel