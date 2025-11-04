import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def calculate_category_breakdown(df, category):
    """
    Kalkulasi breakdown detail per produk dalam kategori
    Mengembalikan dictionary dengan detail Win dan Remaining per jenis produk
    """
    category_data = df[df['Kategori Product High Five'] == category].copy()
    
    if len(category_data) == 0:
        return None
    
    # Group by PRODUCT name
    product_breakdown = {}
    total_products = len(category_data)
    
    for product_name in category_data['PRODUCT'].unique():
        product_data = category_data[category_data['PRODUCT'] == product_name]
        count = len(product_data)
        
        # Hitung rata-rata % Results untuk produk ini
        avg_result = product_data['% Results'].mean() if '% Results' in product_data.columns else 0
        
        product_breakdown[product_name] = {
            'count': count,
            'percentage': (count / total_products) * 100,
            'avg_result': avg_result
        }
    
    return product_breakdown

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

def create_pie_chart_with_breakdown(win_rate, lose_rate, product_breakdown):
    """Create pie chart dengan breakdown detail di tooltip - CLEAN VERSION"""
    
    # Build custom hover text dengan breakdown
    win_breakdown_text = "<b>PROGRESS BREAKDOWN</b><br>"
    remaining_breakdown_text = "<b>REMAINING BREAKDOWN</b><br>"
    
    if product_breakdown:
        # Sort by avg_result descending
        sorted_products = sorted(product_breakdown.items(), key=lambda x: x[1]['avg_result'], reverse=True)
        
        for product_name, data in sorted_products:
            win_contrib = data['avg_result']
            remaining_contrib = 100 - data['avg_result']
            count = data['count']
            
            if win_contrib > 0:
                win_breakdown_text += f"• {product_name}: {count} produk ({win_contrib:.1f}%)<br>"
            
            if remaining_contrib > 0:
                remaining_breakdown_text += f"• {product_name}: {count} produk ({remaining_contrib:.1f}%)<br>"
    
    fig = go.Figure(data=[go.Pie(
        labels=['PROGRESS', 'REMAINING'],
        values=[win_rate, lose_rate],
        hole=0.65,
        marker=dict(
            colors=['#ea1d25', '#e5e7eb'],
            line=dict(color='white', width=3)
        ),
        textinfo='none',
        customdata=[win_breakdown_text, remaining_breakdown_text],
        hovertemplate='<b style="font-size: 15px;">%{label}</b><br>' +
                     '<span style="font-size: 18px; font-weight: 700;">%{value:.1f}%</span><br><br>' +
                     '%{customdata}' +
                     '<extra></extra>',
        pull=[0.05, 0],
        rotation=90
    )])
    
    fig.update_layout(
        showlegend=False,
        height=240,
        margin=dict(t=5, b=5, l=5, r=5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Inter",
            bordercolor="#e5e7eb",
            align="left"
        ),
        annotations=[
            dict(
                text=f'<b style="font-size: 32px; color: #ea1d25;">{win_rate:.1f}%</b><br>' +
                     f'<span style="font-size: 10px; color: #6b7280; font-weight: 600; letter-spacing: 0.5px;">PROGRESS RATE</span>',
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
    
    # Section Header - MODERN DESIGN
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%); 
                padding: 28px 32px; border-radius: 20px; 
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); 
                border: 1px solid #e5e7eb; 
                margin-bottom: 32px;'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;'>
            <div>
                <h2 style='color: #1a202c; margin: 0; font-size: 1.875rem; font-weight: 800; letter-spacing: -0.02em;'>
                    📊 Monitoring Produk Witel
                </h2>
                <p style='color: #6b7280; margin: 10px 0 0 0; font-size: 0.9375rem; font-weight: 500;'>
                    Analisis Progress Rate per Kategori Produk High Five · <b style='color: #ea1d25;'>{selected_witel}</b>
                </p>
            </div>
            <div style='background: linear-gradient(135deg, #ea1d25 0%, #d61921 100%); 
                        padding: 10px 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(234, 29, 37, 0.3);'>
                <span style='color: white; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px;'>
                    💡 HOVER CHART UNTUK DETAIL
                </span>
            </div>
        </div>
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
    
    # Overall statistics - MODERN CARDS
    total_records = len(df)
    total_categories = len(categories)
    overall_avg_result = df['% Results'].dropna().mean() if '% Results' in df.columns else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ea1d25 0%, #d61921 100%); 
                    padding: 24px; border-radius: 18px; 
                    box-shadow: 0 8px 24px rgba(234, 29, 37, 0.25); 
                    text-align: center; border: 2px solid rgba(255,255,255,0.1);
                    position: relative; overflow: hidden;'>
            <div style='position: absolute; top: -30px; right: -30px; 
                        width: 120px; height: 120px; background: rgba(255,255,255,0.08); 
                        border-radius: 50%;'></div>
            <div style='position: relative; z-index: 1;'>
                <div style='color: rgba(255,255,255,0.85); font-size: 0.75rem; font-weight: 700; 
                           text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>
                    Total Records
                </div>
                <div style='color: white; font-size: 2.5rem; font-weight: 900; text-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    {total_records}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                    padding: 24px; border-radius: 18px; 
                    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.25); 
                    text-align: center; border: 2px solid rgba(255,255,255,0.1);
                    position: relative; overflow: hidden;'>
            <div style='position: absolute; top: -30px; right: -30px; 
                        width: 120px; height: 120px; background: rgba(255,255,255,0.08); 
                        border-radius: 50%;'></div>
            <div style='position: relative; z-index: 1;'>
                <div style='color: rgba(255,255,255,0.85); font-size: 0.75rem; font-weight: 700; 
                           text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>
                    Total Kategori
                </div>
                <div style='color: white; font-size: 2.5rem; font-weight: 900; text-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    {total_categories}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #10b981 0%, #047857 100%); 
                    padding: 24px; border-radius: 18px; 
                    box-shadow: 0 8px 24px rgba(16, 185, 129, 0.25); 
                    text-align: center; border: 2px solid rgba(255,255,255,0.1);
                    position: relative; overflow: hidden;'>
            <div style='position: absolute; top: -30px; right: -30px; 
                        width: 120px; height: 120px; background: rgba(255,255,255,0.08); 
                        border-radius: 50%;'></div>
            <div style='position: relative; z-index: 1;'>
                <div style='color: rgba(255,255,255,0.85); font-size: 0.75rem; font-weight: 700; 
                           text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>
                    Avg Progress
                </div>
                <div style='color: white; font-size: 2.5rem; font-weight: 900; text-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    {overall_avg_result:.1f}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Render pie charts - SIMPLE CLEAN
    cols = st.columns(len(categories))
    
    for idx, category in enumerate(categories):
        with cols[idx]:
            win_rate, lose_rate, total_products = calculate_category_win_lose(df, category)
            product_breakdown = calculate_category_breakdown(df, category)
            
            # Category title - BIG & BOLD
            st.markdown(f"""
            <div style='text-align: center; margin-bottom: 8px;'>
                <h3 style='color: #1a202c; margin: 0 0 12px 0; font-size: 1.375rem; 
                          font-weight: 900; letter-spacing: -0.02em;'>
                    {category}
                </h3>
                <div style='background: linear-gradient(135deg, #f5f5f5 0%, #e5e7eb 100%); 
                            padding: 6px 14px; border-radius: 20px; display: inline-block;'>
                    <span style='color: #4a5568; font-size: 0.75rem; font-weight: 700; 
                                letter-spacing: 0.5px;'>
                        📦 {total_products} PRODUK
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Pie chart with hover breakdown
            fig = create_pie_chart_with_breakdown(win_rate, lose_rate, product_breakdown)
            st.plotly_chart(fig, use_container_width=True, key=f"pie_{category}_{idx}", config={'displayModeBar': False})
            
            # Stats Progress & Remaining - SIMPLE
            col_prog, col_rem = st.columns(2)
            with col_prog:
                st.markdown(f"""
                <div style='text-align: center; padding: 12px; 
                            background: linear-gradient(135deg, rgba(234, 29, 37, 0.1) 0%, rgba(234, 29, 37, 0.05) 100%); 
                            border-radius: 12px; border: 2px solid rgba(234, 29, 37, 0.2);'>
                    <div style='color: #ea1d25; font-size: 1.25rem; font-weight: 800;'>
                        {win_rate:.1f}%
                    </div>
                    <div style='color: #6b7280; font-size: 0.65rem; font-weight: 700; 
                               text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px;'>
                        Progress
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_rem:
                st.markdown(f"""
                <div style='text-align: center; padding: 12px; 
                            background: linear-gradient(135deg, #f5f5f5 0%, #e5e7eb 100%); 
                            border-radius: 12px; border: 2px solid #d1d5db;'>
                    <div style='color: #4a5568; font-size: 1.25rem; font-weight: 800;'>
                        {lose_rate:.1f}%
                    </div>
                    <div style='color: #9ca3af; font-size: 0.65rem; font-weight: 700; 
                               text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px;'>
                        Remaining
                    </div>
                </div>
                """, unsafe_allow_html=True)