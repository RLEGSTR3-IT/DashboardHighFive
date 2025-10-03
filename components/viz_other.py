import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def render_other_visualization(filtered_df, selected_witel):
    """
    Render visualisasi tambahan lainnya (extensible section)
    Section ini bisa dikembangkan untuk menampilkan berbagai visualisasi lain
    """
    
    # Section Header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #757575 0%, #616161 100%); 
                padding: 30px 40px; border-radius: 20px; margin-bottom: 30px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);'>
        <div style='display: flex; align-items: center; justify-content: space-between;'>
            <div>
                <h2 style='color: white; margin: 0; font-size: 26px; font-weight: 800;'>
                    📊 Analisis Produk High Five Lainnya
                </h2>
                <p style='color: rgba(255,255,255,0.9); margin: 8px 0 0 0; font-size: 14px;'>
                    Overview semua produk di WITEL {selected_witel}
                </p>
            </div>
        </div>
    </div>
    """.format(selected_witel=selected_witel), unsafe_allow_html=True)
    
    # Analisis produk overview
    product_summary = filtered_df.groupby('PRODUCT HIGH FIVE').agg({
        'CUSTOMER_NAME': 'count',
        'NILAI': 'sum',
        '% Results': 'mean',
        '% Progress': 'mean'
    }).reset_index()
    
    product_summary.columns = ['Product', 'Count', 'Total Value', 'Avg Results', 'Avg Progress']
    product_summary = product_summary.sort_values('Count', ascending=False)
    
    # Metrics untuk produk lainnya
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_products = len(product_summary)
        st.markdown(f"""
        <div style='background: white; padding: 24px 20px; border-radius: 16px; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08); 
                    border-top: 6px solid #757575; height: 140px;'>
            <div style='text-align: center;'>
                <div style='font-size: 36px; margin-bottom: 10px;'>📦</div>
                <div style='color: #757575; font-size: 11px; font-weight: 700; 
                           text-transform: uppercase; letter-spacing: 0.8px; 
                           margin-bottom: 8px;'>
                    TOTAL PRODUK
                </div>
                <div style='color: #757575; font-size: 32px; font-weight: 800;'>
                    {total_products}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_value = product_summary['Total Value'].sum()
        st.markdown(f"""
        <div style='background: white; padding: 24px 20px; border-radius: 16px; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08); 
                    border-top: 6px solid #E60012; height: 140px;'>
            <div style='text-align: center;'>
                <div style='font-size: 36px; margin-bottom: 10px;'>💰</div>
                <div style='color: #757575; font-size: 11px; font-weight: 700; 
                           text-transform: uppercase; letter-spacing: 0.8px; 
                           margin-bottom: 8px;'>
                    TOTAL NILAI
                </div>
                <div style='color: #E60012; font-size: 28px; font-weight: 800;'>
                    {total_value / 1e9:.2f}B
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_progress_all = filtered_df['% Progress'].mean()
        st.markdown(f"""
        <div style='background: white; padding: 24px 20px; border-radius: 16px; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08); 
                    border-top: 6px solid #4CAF50; height: 140px;'>
            <div style='text-align: center;'>
                <div style='font-size: 36px; margin-bottom: 10px;'>📈</div>
                <div style='color: #757575; font-size: 11px; font-weight: 700; 
                           text-transform: uppercase; letter-spacing: 0.8px; 
                           margin-bottom: 8px;'>
                    AVG PROGRESS
                </div>
                <div style='color: #4CAF50; font-size: 32px; font-weight: 800;'>
                    {avg_progress_all:.1f}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Visualisasi dengan 2 kolom
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 24px; border-radius: 16px; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
            <h3 style='color: #757575; margin: 0 0 20px 0; font-size: 20px; 
                      font-weight: 700;'>
                📊 Distribusi Produk
            </h3>
        """, unsafe_allow_html=True)
        
        # Horizontal bar chart untuk produk
        fig_products = go.Figure()
        
        colors = ['#E60012' if i == 0 else '#757575' if i == 1 else '#B0B0B0' 
                  for i in range(len(product_summary))]
        
        fig_products.add_trace(go.Bar(
            y=product_summary['Product'],
            x=product_summary['Count'],
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='white', width=1)
            ),
            text=product_summary['Count'],
            textposition='outside',
            textfont=dict(size=13, family='Inter', weight=700),
            hovertemplate='<b>%{y}</b><br>' +
                         'Jumlah: <b>%{x}</b><br>' +
                         '<extra></extra>'
        ))
        
        fig_products.update_layout(
            height=400,
            margin=dict(t=20, b=20, l=200, r=60),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title='Jumlah',
                titlefont=dict(size=12, family='Inter', color='#757575'),
                gridcolor='#F0F0F0',
                showline=False,
                zeroline=False,
                tickfont=dict(size=11, family='Inter', color='#757575')
            ),
            yaxis=dict(
                showgrid=False,
                showline=False,
                tickfont=dict(size=11, family='Inter', color='#333')
            ),
            font=dict(family='Inter')
        )
        
        st.plotly_chart(fig_products, use_container_width=True, key="products_bar")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 24px; border-radius: 16px; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
            <h3 style='color: #757575; margin: 0 0 20px 0; font-size: 20px; 
                      font-weight: 700;'>
                💰 Nilai per Produk
            </h3>
        """, unsafe_allow_html=True)
        
        # Donut chart untuk nilai produk
        fig_value = go.Figure(data=[go.Pie(
            labels=product_summary['Product'],
            values=product_summary['Total Value'],
            hole=0.5,
            marker=dict(
                colors=['#E60012', '#757575', '#B0B0B0', '#D0D0D0', '#E8E8E8'],
                line=dict(color='white', width=3)
            ),
            textinfo='label+percent',
            textfont=dict(size=11, family='Inter', weight=600),
            textposition='outside',
            hovertemplate='<b>%{label}</b><br>' +
                         'Nilai: Rp %{value:,.0f}<br>' +
                         'Persentase: %{percent}<br>' +
                         '<extra></extra>'
        )])
        
        total_value_text = f"Rp {total_value/1e9:.1f}B"
        
        fig_value.update_layout(
            showlegend=False,
            height=400,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(
                    text=f'<b style="font-size: 24px; color: #E60012;">{total_value_text}</b><br>' +
                         f'<span style="font-size: 12px; color: #757575;">TOTAL NILAI</span>',
                    x=0.5, y=0.5,
                    font=dict(family='Inter'),
                    showarrow=False,
                    align='center'
                )
            ]
        )
        
        st.plotly_chart(fig_value, use_container_width=True, key="value_pie")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Tabel detail semua produk
    st.markdown("""
    <div style='background: white; padding: 30px; border-radius: 16px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
        <div style='display: flex; justify-content: space-between; align-items: center; 
                    margin-bottom: 24px;'>
            <h3 style='color: #757575; margin: 0; font-size: 20px; font-weight: 700;'>
                📋 Summary Per Produk
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Format untuk display
    display_summary = product_summary.copy()
    display_summary['Total Value'] = display_summary['Total Value'].apply(
        lambda x: f"Rp {x/1e9:.2f}B" if pd.notna(x) else "-"
    )
    display_summary['Avg Results'] = display_summary['Avg Results'].apply(
        lambda x: f"{x:.1f}%" if pd.notna(x) else "-"
    )
    display_summary['Avg Progress'] = display_summary['Avg Progress'].apply(
        lambda x: f"{x:.1f}%" if pd.notna(x) else "-"
    )
    
    st.dataframe(
        display_summary,
        use_container_width=True,
        height=300,
        column_config={
            "Product": st.column_config.TextColumn(
                "Product High Five",
                width="large",
            ),
            "Count": st.column_config.NumberColumn(
                "Jumlah",
                format="%d",
                width="small",
            ),
            "Total Value": st.column_config.TextColumn(
                "Total Nilai",
                width="medium",
            ),
            "Avg Results": st.column_config.TextColumn(
                "Avg Results",
                width="small",
            ),
            "Avg Progress": st.column_config.TextColumn(
                "Avg Progress",
                width="small",
            )
        },
        hide_index=True
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Info box untuk extensibility
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(117, 117, 117, 0.1) 0%, rgba(97, 97, 97, 0.1) 100%); 
                padding: 20px 30px; border-radius: 12px; border-left: 6px solid #757575;'>
        <div style='display: flex; align-items: center;'>
            <span style='font-size: 28px; margin-right: 16px;'>💡</span>
            <div>
                <div style='color: #757575; font-size: 14px; font-weight: 700; margin-bottom: 4px;'>
                    EXTENSIBLE SECTION
                </div>
                <div style='color: #999; font-size: 12px;'>
                    Section ini dapat dikembangkan lebih lanjut dengan menambahkan visualisasi lain 
                    sesuai kebutuhan analisis
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)