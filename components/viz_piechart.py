import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def calculate_category_win_lose(df, category):
    """
    Kalkulasi Win/Lose rate untuk sebuah kategori produk
    Win = rata-rata % Results dari semua produk dalam kategori
    Lose = 100% - Win
    """
    category_data = df[df['Kategori Product High Five'] == category]
    
    if len(category_data) > 0:
        valid_results = category_data['% Results'].dropna()
        
        if len(valid_results) > 0:
            avg_result = valid_results.mean()
            win_rate = avg_result
            lose_rate = 100 - avg_result
            return win_rate, lose_rate, len(category_data)
    
    return 0, 100, 0

def create_pie_chart(win_rate, lose_rate):
    """Create pie chart untuk satu kategori - FIXED PARAMETER"""
    
    fig = go.Figure(data=[go.Pie(
        labels=['PROGRESS', 'REMAINING'],
        values=[win_rate, lose_rate],
        hole=0.65,
        marker=dict(
            colors=['#ea1d25', '#e1e7ef'],
            line=dict(color='white', width=2)
        ),
        textinfo='none',
        hovertemplate='<b style="font-size: 12px;">%{label}</b><br>' +
                     '<span style="font-size: 14px; font-weight: 700;">%{value:.1f}%</span>' +
                     '<extra></extra>',
        pull=[0.03, 0],
        rotation=90
    )])
    
    fig.update_layout(
        showlegend=False,
        height=220,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[
            dict(
                text=f'<b style="font-size: 28px; color: #ea1d25;">{win_rate:.1f}%</b><br>' +
                     f'<span style="font-size: 9px; color: #6b7280; font-weight: 600; letter-spacing: 0.5px;">PROGRESS RATE</span>',
                x=0.5, y=0.5,
                font=dict(family='Inter'),
                showarrow=False,
                align='center'
            )
        ]
    )
    
    return fig

def render_piechart_visualization(df, selected_witel):
    """Render section visualisasi pie chart per kategori produk untuk WITEL tertentu"""
    
    # Section Header dalam CARD PUTIH
    st.markdown(f"""
    <div style='background: white; padding: 20px 24px; border-radius: 20px; 
                box-shadow: 0 1px 3px 0 rgba(16, 24, 40, 0.04); border: 1px solid #e1e7ef; margin-bottom: 24px;'>
        <h2 style='color: #2d3748; margin: 0; font-size: 1.75rem; font-weight: 700; letter-spacing: -0.02em;'>
            Monitoring Produk Witel
        </h2>
        <p style='color: #6b7280; margin: 8px 0 0 0; font-size: 0.875rem; font-weight: 500;'>
            Analisis Progress Rate per Kategori Produk High Five - <b>{selected_witel}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Validasi kolom yang diperlukan
    required_columns = ['Kategori Product High Five', 'PRODUCT', '% Results']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Kolom yang diperlukan tidak ditemukan: {', '.join(missing_columns)}")
        st.info("Pastikan sheet memiliki kolom: Kategori Product High Five, PRODUCT, % Results")
        return
    
    # Get unique categories
    categories = df['Kategori Product High Five'].dropna().unique()
    
    if len(categories) == 0:
        st.warning("Tidak ada kategori produk yang ditemukan di data")
        return
    
    # Overall statistics TANPA EMOJI
    total_records = len(df)
    total_categories = len(categories)
    overall_avg_result = df['% Results'].dropna().mean() if '% Results' in df.columns else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ea1d25 0%, #d61921 100%); 
                    padding: 20px; border-radius: 16px; 
                    box-shadow: 0 4px 12px rgba(234, 29, 37, 0.2); text-align: center;'>
            <div style='color: rgba(255,255,255,0.9); font-size: 0.7rem; font-weight: 600; 
                       text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;'>
                Total Records
            </div>
            <div style='color: white; font-size: 2rem; font-weight: 800;'>
                {total_records}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #6b7280 0%, #4a5568 100%); 
                    padding: 20px; border-radius: 16px; 
                    box-shadow: 0 4px 12px rgba(107, 114, 128, 0.2); text-align: center;'>
            <div style='color: rgba(255,255,255,0.9); font-size: 0.7rem; font-weight: 600; 
                       text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;'>
                Total Kategori
            </div>
            <div style='color: white; font-size: 2rem; font-weight: 800;'>
                {total_categories}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #10b981 0%, #047857 100%); 
                    padding: 20px; border-radius: 16px; 
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2); text-align: center;'>
            <div style='color: rgba(255,255,255,0.9); font-size: 0.7rem; font-weight: 600; 
                       text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;'>
                Avg Progress
            </div>
            <div style='color: white; font-size: 2rem; font-weight: 800;'>
                {overall_avg_result:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Render pie charts
    cols = st.columns(len(categories))
    
    for idx, category in enumerate(categories):
        with cols[idx]:
            win_rate, lose_rate, total_products = calculate_category_win_lose(df, category)
            
            # Nama kategori dan badge (tanpa card)
            st.markdown(f"""
            <div style='margin-bottom: 16px;'>
                <h3 style='color: #2d3748; margin: 0 0 8px 0; font-size: 1.1rem; 
                          font-weight: 700; text-align: center; letter-spacing: -0.01em;'>
                    {category}
                </h3>
                <div style='background: linear-gradient(135deg, #f4f6f8 0%, #e1e7ef 100%); 
                            padding: 6px 14px; border-radius: 20px; text-align: center;'>
                    <span style='color: #6b7280; font-size: 0.75rem; font-weight: 700; 
                                letter-spacing: 0.5px;'>
                        {total_products} PRODUK
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Pie chart LANGSUNG tanpa card putih
            fig = create_pie_chart(win_rate, lose_rate)
            st.plotly_chart(fig, use_container_width=True, key=f"pie_{category}_{idx}", config={'displayModeBar': False})
            
            # Stats Progress & Remaining
            col_prog, col_rem = st.columns(2)
            with col_prog:
                st.markdown(f"""
                <div style='text-align: center; padding: 10px; 
                            background: rgba(234, 29, 37, 0.08); 
                            border-radius: 8px; border: 1px solid rgba(234, 29, 37, 0.2);'>
                    <div style='color: #ea1d25; font-size: 1.15rem; font-weight: 700;'>
                        {win_rate:.1f}%
                    </div>
                    <div style='color: #6b7280; font-size: 0.65rem; font-weight: 600; 
                               text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px;'>
                        Progress
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_rem:
                st.markdown(f"""
                <div style='text-align: center; padding: 10px; 
                            background: #f4f6f8; 
                            border-radius: 8px; border: 1px solid #e1e7ef;'>
                    <div style='color: #6b7280; font-size: 1.15rem; font-weight: 700;'>
                        {lose_rate:.1f}%
                    </div>
                    <div style='color: #9ca3af; font-size: 0.65rem; font-weight: 600; 
                               text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px;'>
                        Remaining
                    </div>
                </div>
                """, unsafe_allow_html=True)