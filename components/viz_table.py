import streamlit as st
import pandas as pd

def format_currency(value):
    """Format nilai menjadi format currency Indonesia"""
    if pd.isna(value) or value == 0:
        return "Rp 0"
    return f"Rp {value:,.0f}".replace(",", ".")

def get_progress_color(progress):
    """Dapatkan warna berdasarkan progress"""
    if pd.isna(progress):
        return "#9ca3af"
    elif progress >= 75:
        return "#10b981"
    elif progress >= 50:
        return "#f59e0b"
    elif progress >= 25:
        return "#3b82f6"
    else:
        return "#ef4444"

def get_progress_label(progress):
    """Dapatkan label status berdasarkan progress"""
    if pd.isna(progress):
        return "Belum Dimulai"
    elif progress >= 75:
        return "Hampir Selesai"
    elif progress >= 50:
        return "Sedang Berlangsung"
    elif progress >= 25:
        return "Baru Dimulai"
    else:
        return "Perlu Perhatian"

def render_table_visualization(df, selected_witel):
    """Render visualisasi progress Account Manager dengan modern card design"""
    
    # Section Header dalam CARD PUTIH seperti viz_piechart
    st.markdown(f"""
    <div style='background: white; padding: 20px 24px; border-radius: 20px; 
                box-shadow: 0 1px 3px 0 rgba(16, 24, 40, 0.04); border: 1px solid #e1e7ef; margin-bottom: 24px;'>
        <h2 style='color: #2d3748; margin: 0; font-size: 1.75rem; font-weight: 700; letter-spacing: -0.02em;'>
            📊 Progress Account Manager
        </h2>
        <p style='color: #6b7280; margin: 8px 0 0 0; font-size: 0.875rem; font-weight: 500;'>
            Monitoring detail progress setiap Account Manager beserta customer dan produk yang dihandle - <b>{selected_witel}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Prepare data - group by AM
    am_groups = df.groupby('AM').agg({
        'CUSTOMER_NAME': 'nunique',
        'PRODUCT': 'count',
        'NILAI': 'sum',
        '% Progress': 'mean'
    }).reset_index()
    
    am_groups.columns = ['AM', 'Total_Customers', 'Total_Products', 'Total_Nilai', 'Avg_Progress']
    am_groups = am_groups.sort_values('Total_Nilai', ascending=False)
    
    # Summary cards - SAMA SEPERTI VIZ_PIECHART
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ea1d25 0%, #d61921 100%); 
                    padding: 20px; border-radius: 16px; 
                    box-shadow: 0 4px 12px rgba(234, 29, 37, 0.2); text-align: center;'>
            <div style='color: rgba(255,255,255,0.9); font-size: 0.7rem; font-weight: 600; 
                       text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;'>
                Total Account Manager
            </div>
            <div style='color: white; font-size: 2rem; font-weight: 800;'>
                {len(am_groups)}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_customers = df['CUSTOMER_NAME'].nunique()
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                    padding: 20px; border-radius: 16px; 
                    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2); text-align: center;'>
            <div style='color: rgba(255,255,255,0.9); font-size: 0.7rem; font-weight: 600; 
                       text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;'>
                Total Customer
            </div>
            <div style='color: white; font-size: 2rem; font-weight: 800;'>
                {total_customers}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_products = len(df)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #6b7280 0%, #4a5568 100%); 
                    padding: 20px; border-radius: 16px; 
                    box-shadow: 0 4px 12px rgba(107, 114, 128, 0.2); text-align: center;'>
            <div style='color: rgba(255,255,255,0.9); font-size: 0.7rem; font-weight: 600; 
                       text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;'>
                Total Produk
            </div>
            <div style='color: white; font-size: 2rem; font-weight: 800;'>
                {total_products}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_progress = df['% Progress'].mean()
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #10b981 0%, #047857 100%); 
                    padding: 20px; border-radius: 16px; 
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2); text-align: center;'>
            <div style='color: rgba(255,255,255,0.9); font-size: 0.7rem; font-weight: 600; 
                       text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;'>
                Avg Progress
            </div>
            <div style='color: white; font-size: 2rem; font-weight: 800;'>
                {avg_progress:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render setiap AM dengan COMPACT design
    for idx, am_row in am_groups.iterrows():
        am_name = am_row['AM']
        am_data = df[df['AM'] == am_name].copy()
        prog_val = am_row['Avg_Progress']
        
        # AM Card Header - COMPACT
        with st.expander(
            f"**{am_name}** - {am_row['Total_Customers']} Customer | {am_row['Total_Products']} Produk | Progress: {prog_val:.1f}%",
            expanded=False
        ):
            # AM Summary Row - COMPACT
            col_a, col_b = st.columns([1, 1])
            
            with col_a:
                st.markdown(f"""
                <div style='background: linear-gradient(to right, #ea1d25 0%, #ea1d25 {prog_val}%, #e1e7ef {prog_val}%, #e1e7ef 100%); 
                            height: 6px; border-radius: 3px; margin-bottom: 8px;'></div>
                <div style='color: #6b7280; font-size: 0.8rem;'>
                    Total Nilai: <span style='color: #ea1d25; font-weight: 700; font-size: 1rem;'>{format_currency(am_row['Total_Nilai'])}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"""
                <div style='text-align: right; padding-top: 14px;'>
                    <span style='background: {get_progress_color(prog_val)}; color: white; 
                                padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; 
                                font-weight: 700;'>
                        {get_progress_label(prog_val)}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Group by customer - COMPACT LAYOUT
            for customer_name in am_data['CUSTOMER_NAME'].unique():
                customer_data = am_data[am_data['CUSTOMER_NAME'] == customer_name]
                
                # Customer Header - COMPACT dengan gap lebih besar
                st.markdown(f"""
                <div style='background: white; border-left: 4px solid #ea1d25; 
                            padding: 14px 18px; margin-bottom: 8px; margin-top: 20px; border-radius: 8px;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.06);'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <span style='color: #2d3748; font-weight: 800; font-size: 1.05rem; font-family: "Inter", sans-serif;'>🏢 {customer_name}</span>
                            <span style='color: #9ca3af; font-size: 0.75rem; font-weight: 600; margin-left: 8px;'>({len(customer_data)} Produk)</span>
                        </div>
                        <div style='color: #ea1d25; font-weight: 800; font-size: 1rem;'>
                            {format_currency(customer_data['NILAI'].sum())}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Product items - SUPER COMPACT TABLE STYLE
                for _, prod_row in customer_data.iterrows():
                    progress = prod_row.get('% Progress', 0)
                    if pd.isna(progress):
                        progress = 0
                    
                    result = prod_row.get('% Results', 0)
                    if pd.isna(result):
                        result = 0
                    
                    progress_status = prod_row.get('Progress', '-')
                    result_status = prod_row.get('Result', '-')
                    
                    st.markdown(f"""
                    <div style='background: #f9fafb; padding: 10px 14px; margin-bottom: 6px; 
                                border-radius: 6px; border-left: 3px solid {get_progress_color(progress)};'>
                        <div style='display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 12px; align-items: center;'>
                            <div>
                                <div style='color: #2d3748; font-weight: 600; font-size: 0.9rem;'>
                                    📦 {prod_row['PRODUCT']}
                                </div>
                                <div style='color: #9ca3af; font-size: 0.7rem;'>
                                    {format_currency(prod_row['NILAI'])}
                                </div>
                            </div>
                            <div style='text-align: center;'>
                                <div style='color: {get_progress_color(progress)}; font-weight: 700; font-size: 0.95rem;'>
                                    {progress:.0f}%
                                </div>
                                <div style='color: #9ca3af; font-size: 0.65rem;'>Progress</div>
                            </div>
                            <div style='text-align: center;'>
                                <div style='color: #6b7280; font-weight: 700; font-size: 0.95rem;'>
                                    {result:.0f}%
                                </div>
                                <div style='color: #9ca3af; font-size: 0.65rem;'>Result</div>
                            </div>
                            <div style='text-align: center;'>
                                <div style='color: #4a5568; font-size: 0.75rem; font-weight: 600;'>
                                    {progress_status}
                                </div>
                            </div>
                        </div>
                        <div style='margin-top: 8px;'>
                            <div style='background: #e1e7ef; height: 4px; border-radius: 2px; overflow: hidden;'>
                                <div style='background: {get_progress_color(progress)}; height: 100%; width: {progress}%;'></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Table view option - COMPACT
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 View Tabel Detail"):
        table_data = df[['AM', 'CUSTOMER_NAME', 'PRODUCT', 'NILAI', '% Progress', '% Results', 'Progress', 'Result']].copy()
        table_data = table_data.sort_values(['AM', 'CUSTOMER_NAME', 'PRODUCT'])
        
        display_data = table_data.copy()
        display_data['NILAI'] = display_data['NILAI'].apply(format_currency)
        display_data['% Progress'] = display_data['% Progress'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "0%")
        display_data['% Results'] = display_data['% Results'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "0%")
        
        st.dataframe(
            display_data,
            use_container_width=True,
            height=400,
            hide_index=True
        )