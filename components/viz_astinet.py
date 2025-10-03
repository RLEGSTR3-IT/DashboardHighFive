import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def calculate_win_lose(filtered_df):
    """Calculate average % Results untuk Astinet Bundling DDoS"""
    astinet_data = filtered_df[filtered_df['PRODUCT HIGH FIVE'] == 'Astinet Bundling DDoS']
    
    if len(astinet_data) > 0:
        # Filter out NaN values
        valid_results = astinet_data['% Results'].dropna()
        
        if len(valid_results) > 0:
            avg_result = valid_results.mean()
            win_rate = avg_result
            lose_rate = 100 - avg_result
            return win_rate, lose_rate, len(astinet_data)
    
    return 0, 0, 0

def render_astinet_visualization(filtered_df, selected_witel):
    """Render visualisasi untuk Astinet Bundling DDoS"""
    
    # Calculate metrics
    win_rate, lose_rate, total_records = calculate_win_lose(filtered_df)
    
    # Section Header dengan design modern
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #E60012 0%, #C4000F 100%); 
                padding: 30px 40px; border-radius: 20px; margin-bottom: 30px;
                box-shadow: 0 8px 32px rgba(230, 0, 18, 0.3);'>
        <div style='display: flex; align-items: center; justify-content: space-between;'>
            <div>
                <h2 style='color: white; margin: 0; font-size: 28px; font-weight: 800;'>
                    📍 {selected_witel}
                </h2>
                <p style='color: rgba(255,255,255,0.9); margin: 8px 0 0 0; font-size: 14px;'>
                    Dashboard Monitoring Astinet Bundling DDoS
                </p>
            </div>
            <div style='background: rgba(255,255,255,0.2); padding: 12px 24px; 
                        border-radius: 12px; backdrop-filter: blur(10px);'>
                <span style='color: white; font-size: 12px; font-weight: 600; 
                            letter-spacing: 0.5px;'>
                    REAL-TIME DATA
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics Row dengan card modern
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_data = [
        ("📊", "TOTAL DATA", len(filtered_df), "#E60012", "Total records di WITEL ini"),
        ("🎯", "ASTINET BUNDLING", total_records, "#757575", "Jumlah Astinet Bundling DDoS"),
        ("✅", "WIN RATE", f"{win_rate:.1f}%", "#4CAF50", "Rata-rata % Results"),
        ("❌", "LOSE RATE", f"{lose_rate:.1f}%", "#FF5252", "Sisa dari WIN Rate")
    ]
    
    for col, (icon, label, value, color, desc) in zip([col1, col2, col3, col4], metrics_data):
        with col:
            st.markdown(f"""
            <div style='background: white; padding: 24px 20px; border-radius: 16px; 
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08); 
                        border-top: 6px solid {color};
                        transition: all 0.3s ease; height: 160px;'>
                <div style='text-align: center;'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>{icon}</div>
                    <div style='color: #757575; font-size: 11px; font-weight: 700; 
                               text-transform: uppercase; letter-spacing: 0.8px; 
                               margin-bottom: 8px;'>
                        {label}
                    </div>
                    <div style='color: {color}; font-size: 32px; font-weight: 800; 
                               margin-bottom: 4px;'>
                        {value}
                    </div>
                    <div style='color: #999; font-size: 10px;'>
                        {desc}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ========== VISUALISASI ==========
    
    if total_records > 0:
        # Create two columns for charts
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown("""
            <div style='background: white; padding: 24px; border-radius: 16px; 
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
                <h3 style='color: #E60012; margin: 0 0 20px 0; font-size: 20px; 
                          font-weight: 700;'>
                    🥧 Win vs Lose Rate
                </h3>
            """, unsafe_allow_html=True)
            
            # Enhanced Pie Chart
            fig_pie = go.Figure(data=[go.Pie(
                labels=['WIN', 'LOSE'],
                values=[win_rate, lose_rate],
                hole=0.6,
                marker=dict(
                    colors=['#E60012', '#E8E8E8'],
                    line=dict(color='white', width=4)
                ),
                textinfo='label+percent',
                textfont=dict(size=15, color='#333', family='Inter', weight=700),
                textposition='outside',
                hovertemplate='<b style="font-size: 14px;">%{label}</b><br>' +
                             '<span style="font-size: 16px; font-weight: 700;">%{value:.1f}%</span>' +
                             '<extra></extra>',
                pull=[0.05, 0],
                rotation=90
            )])
            
            fig_pie.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=13, family='Inter', color='#757575'),
                    itemsizing='constant'
                ),
                height=450,
                margin=dict(t=20, b=60, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                annotations=[
                    dict(
                        text=f'<b style="font-size: 42px; color: #E60012;">{win_rate:.1f}%</b><br>' +
                             f'<span style="font-size: 16px; color: #757575; font-weight: 600;">WIN RATE</span>',
                        x=0.5, y=0.5,
                        font=dict(family='Inter'),
                        showarrow=False,
                        align='center'
                    )
                ]
            )
            
            st.plotly_chart(fig_pie, use_container_width=True, key="pie_chart")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: white; padding: 24px; border-radius: 16px; 
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
                <h3 style='color: #E60012; margin: 0 0 20px 0; font-size: 20px; 
                          font-weight: 700;'>
                    📊 Performance Breakdown
                </h3>
            """, unsafe_allow_html=True)
            
            # Modern bar chart with gradient
            fig_bar = go.Figure()
            
            fig_bar.add_trace(go.Bar(
                x=['WIN', 'LOSE'],
                y=[win_rate, lose_rate],
                marker=dict(
                    color=['#E60012', '#E8E8E8'],
                    line=dict(color='white', width=2),
                    pattern_shape=['', '']
                ),
                text=[f'{win_rate:.1f}%', f'{lose_rate:.1f}%'],
                textposition='outside',
                textfont=dict(size=18, family='Inter', weight=700, color='#333'),
                hovertemplate='<b style="font-size: 14px;">%{x}</b><br>' +
                             '<span style="font-size: 16px; font-weight: 700;">%{y:.1f}%</span>' +
                             '<extra></extra>',
                width=[0.5, 0.5]
            ))
            
            fig_bar.update_layout(
                height=450,
                margin=dict(t=20, b=80, l=40, r=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(
                    title='Percentage (%)',
                    titlefont=dict(size=12, family='Inter', color='#757575'),
                    range=[0, 110],
                    gridcolor='#F0F0F0',
                    showline=False,
                    zeroline=False,
                    tickfont=dict(size=11, family='Inter', color='#757575')
                ),
                xaxis=dict(
                    showgrid=False,
                    showline=False,
                    tickfont=dict(size=14, family='Inter', weight=700, color='#333')
                ),
                font=dict(family='Inter'),
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=13,
                    font_family="Inter"
                )
            )
            
            st.plotly_chart(fig_bar, use_container_width=True, key="bar_chart")
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Detail table dengan styling modern
        st.markdown("""
        <div style='background: white; padding: 30px; border-radius: 16px; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
            <div style='display: flex; justify-content: space-between; align-items: center; 
                        margin-bottom: 24px;'>
                <h3 style='color: #E60012; margin: 0; font-size: 20px; font-weight: 700;'>
                    📋 Detail Astinet Bundling DDoS
                </h3>
                <span style='background: linear-gradient(135deg, #E60012 0%, #C4000F 100%); 
                            color: white; padding: 8px 16px; border-radius: 20px; 
                            font-size: 12px; font-weight: 700; letter-spacing: 0.5px;'>
                    {total_records} RECORDS
                </span>
            </div>
        """.format(total_records=total_records), unsafe_allow_html=True)
        
        astinet_detail = filtered_df[filtered_df['PRODUCT HIGH FIVE'] == 'Astinet Bundling DDoS'][
            ['CUSTOMER_NAME', 'AM', 'NILAI', '% Progress', '% Results', 'Result']
        ].sort_values('% Results', ascending=False).copy()
        
        # Format NILAI as currency - Convert to numeric first
        if 'NILAI' in astinet_detail.columns:
            astinet_detail['NILAI'] = pd.to_numeric(astinet_detail['NILAI'], errors='coerce')
            astinet_detail['NILAI'] = astinet_detail['NILAI'].apply(
                lambda x: f"Rp {x:,.0f}".replace(',', '.') if pd.notna(x) else "-"
            )
        
        st.dataframe(
            astinet_detail,
            use_container_width=True,
            height=400,
            column_config={
                "CUSTOMER_NAME": st.column_config.TextColumn(
                    "Customer Name",
                    width="medium",
                ),
                "AM": st.column_config.TextColumn(
                    "Account Manager",
                    width="medium",
                ),
                "NILAI": st.column_config.TextColumn(
                    "Nilai Kontrak",
                    width="small",
                ),
                "% Progress": st.column_config.ProgressColumn(
                    "Progress",
                    format="%.0f%%",
                    min_value=0,
                    max_value=100,
                    width="small",
                ),
                "% Results": st.column_config.ProgressColumn(
                    "Results",
                    format="%.0f%%",
                    min_value=0,
                    max_value=100,
                    width="small",
                ),
                "Result": st.column_config.TextColumn(
                    "Status",
                    width="small",
                )
            },
            hide_index=True
        )
        
        # Download button
        st.markdown("<br>", unsafe_allow_html=True)
        csv = astinet_detail.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data CSV",
            data=csv,
            file_name=f"astinet_bundling_{selected_witel.lower().replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div style='background: white; padding: 40px; border-radius: 16px; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08); text-align: center;'>
            <div style='font-size: 64px; margin-bottom: 16px;'>📊</div>
            <h3 style='color: #757575; margin: 0 0 12px 0;'>
                Tidak Ada Data Astinet Bundling DDoS
            </h3>
            <p style='color: #999; margin: 0;'>
                Untuk WITEL <b style='color: #E60012;'>{selected_witel}</b>
            </p>
        </div>
        """.format(selected_witel=selected_witel), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tampilkan semua data witel tersebut
        st.markdown("""
        <div style='background: white; padding: 30px; border-radius: 16px; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
            <h3 style='color: #757575; margin: 0 0 20px 0;'>
                📋 Semua Data di WITEL ini
            </h3>
        """, unsafe_allow_html=True)
        
        st.dataframe(filtered_df, use_container_width=True, height=400, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)