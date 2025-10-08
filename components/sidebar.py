import base64, io
from pathlib import Path

import streamlit as st
from PIL import Image, ImageFile

# Amanin pembacaan gambar besar
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

# List Witel
WITEL_LIST = [
    "JATIM BARAT",
    "YOGYA JATENG SELATAN",
    "SEMARANG JATENG UTARA",
    "SURAMADU",
    "BALI",
    "NUSA TENGGARA",
    "JATIM TIMUR",
    "SOLO JATENG TIMUR",
]

def _safe_logo(img_path: Path, width_px: int = 260, top_gap: int = 50):
    """
    Render logo: center, jarak dari atas 'top_gap' px, lebar 'width_px' px.
    Resize di runtime + fallback base64 agar lolos limit Pillow/versi Streamlit.
    """
    try:
        with Image.open(img_path) as img:
            img = img.convert("RGBA")
            if img.width > width_px:
                r = width_px / float(img.width)
                img = img.resize((width_px, int(img.height * r)), Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            b64 = base64.b64encode(buf.getvalue()).decode()
    except Exception:
        # fallback baca langsung file
        b64 = base64.b64encode(open(img_path, "rb").read()).decode()

    st.markdown(
        f"""
        <div style="text-align:center; margin-top:{top_gap}px;">
            <img src="data:image/png;base64,{b64}" style="width:{width_px}px; height:auto;" />
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar():
    """Render sidebar: logo + filter WITEL + tombol refresh"""
    with st.sidebar:
        # 1) LOGO
        logo_path = Path("assets/telkom.png")
        if logo_path.exists():
            _safe_logo(logo_path, width_px=260, top_gap=50)
        else:
            st.markdown(
                """
                <div style='text-align:center; margin-top:50px;'>
                  <h2 style='color:#fff; margin:0;'>HIGH FIVE</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Garis pembatas
        st.markdown(
            """
            <div style='border-top: 2px solid rgba(255,255,255,0.3);
                        margin: 30px -20px 30px -20px;'></div>
            """,
            unsafe_allow_html=True,
        )

        # 2) FILTER WITEL
        st.markdown(
            """
            <p style='color:#fff; font-size:13px; font-weight:700; margin-bottom:8px; letter-spacing:.5px;'>
              📍 PILIH WITEL
            </p>
            """,
            unsafe_allow_html=True,
        )

        selected_witel = st.selectbox(
            "witel_select",
            options=["-- Pilih Witel --"] + WITEL_LIST,
            key="witel_filter",
            label_visibility="collapsed",
        )

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # 3) REFRESH
        if st.button("🔄 REFRESH DATA", use_container_width=True, key="refresh_btn"):
            st.cache_data.clear()
            st.rerun()

        return selected_witel
