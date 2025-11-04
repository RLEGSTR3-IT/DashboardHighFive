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

def render_card_mode(df, am_groups):
    """Render Card Mode - Clean design without gradient"""
    
    for idx, am_row in am_groups.iterrows():
        am_name = am_row['AM']
        am_data = df[df['AM'] == am_name].copy()
        prog_val = am_row['Avg_Progress']
        
        # AM Card with clean design
        with st.expander(
            f"**{am_name}** - {am_row['Total_Customers']} Customer | {am_row['Total_Products']} Produk | Progress: {prog_val:.1f}%",
            expanded=False
        ):
            # AM Summary Row
            col_a, col_b = st.columns([1, 1])
            
            with col_a:
                st.markdown(f"""
                <div style='background: #ea1d25; 
                            height: 8px; border-radius: 4px; margin-bottom: 12px; width: {prog_val}%;'></div>
                <div style='color: #4a5568; font-size: 0.875rem; font-weight: 500;'>
                    Total Nilai: <span style='color: #ea1d25; font-weight: 800; font-size: 1.125rem;'>{format_currency(am_row['Total_Nilai'])}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"""
                <div style='text-align: right; padding-top: 16px;'>
                    <span style='background: {get_progress_color(prog_val)}; color: white; 
                                padding: 6px 16px; border-radius: 16px; font-size: 0.8125rem; 
                                font-weight: 700; display: inline-block;
                                box-shadow: 0 2px 8px {get_progress_color(prog_val)}30;'>
                        {get_progress_label(prog_val)}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Customer sections
            for customer_name in am_data['CUSTOMER_NAME'].unique():
                customer_data = am_data[am_data['CUSTOMER_NAME'] == customer_name]
                
                st.markdown(f"""
                <div style='background: #ffffff; border-left: 5px solid #ea1d25; 
                            padding: 16px 20px; margin-bottom: 10px; margin-top: 24px; border-radius: 10px;
                            box-shadow: 0 2px 6px rgba(0,0,0,0.08); border: 1px solid #e5e7eb;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;'>
                        <div style='flex: 1; min-width: 200px;'>
                            <div style='color: #1a202c; font-weight: 800; font-size: 1.125rem; margin-bottom: 4px;'>
                                🏢 {customer_name}
                            </div>
                            <div style='color: #9ca3af; font-size: 0.8125rem; font-weight: 600;'>
                                {len(customer_data)} Produk
                            </div>
                        </div>
                        <div style='text-align: right;'>
                            <div style='color: #ea1d25; font-weight: 900; font-size: 1.25rem;'>
                                {format_currency(customer_data['NILAI'].sum())}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Products for this customer
                for _, prod_row in customer_data.iterrows():
                    progress = prod_row.get('% Progress', 0)
                    if pd.isna(progress):
                        progress = 0
                    
                    result = prod_row.get('% Results', 0)
                    if pd.isna(result):
                        result = 0
                    
                    progress_status = prod_row.get('Progress', '-')
                    if pd.isna(progress_status) or str(progress_status) == 'nan':
                        progress_status = '-'
                    
                    st.markdown(f"""
                    <div style='background: #f9fafb; padding: 14px 16px; margin-bottom: 8px; 
                                border-radius: 8px; border-left: 4px solid {get_progress_color(progress)};
                                border: 1px solid #e5e7eb; border-left: 4px solid {get_progress_color(progress)};'>
                        <div style='display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 16px; align-items: center;'>
                            <div>
                                <div style='color: #1a202c; font-weight: 700; font-size: 0.9375rem; margin-bottom: 4px;'>
                                    📦 {prod_row['PRODUCT']}
                                </div>
                                <div style='color: #6b7280; font-size: 0.75rem; font-weight: 500;'>
                                    {format_currency(prod_row['NILAI'])}
                                </div>
                            </div>
                            <div style='text-align: center;'>
                                <div style='color: {get_progress_color(progress)}; font-weight: 800; font-size: 1.0625rem;'>
                                    {progress:.0f}%
                                </div>
                                <div style='color: #9ca3af; font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;'>
                                    Progress
                                </div>
                            </div>
                            <div style='text-align: center;'>
                                <div style='color: #4a5568; font-weight: 800; font-size: 1.0625rem;'>
                                    {result:.0f}%
                                </div>
                                <div style='color: #9ca3af; font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;'>
                                    Result
                                </div>
                            </div>
                            <div style='text-align: center;'>
                                <div style='background: #e5e7eb; color: #4a5568; padding: 4px 10px; 
                                           border-radius: 6px; font-size: 0.75rem; font-weight: 700; display: inline-block;'>
                                    {progress_status}
                                </div>
                            </div>
                        </div>
                        <div style='margin-top: 12px;'>
                            <div style='background: #e5e7eb; height: 6px; border-radius: 3px; overflow: hidden;'>
                                <div style='background: {get_progress_color(progress)}; height: 100%; width: {progress}%; 
                                           transition: width 0.3s ease;'></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

def render_table_mode(df):
    """Render Table Mode - Full dataframe view"""
    
    st.markdown("#### 📋 Tabel Detail Semua Data")
    
    # Prepare display data
    display_data = df[['AM', 'CUSTOMER_NAME', 'PRODUCT', 'NILAI', '% Progress', '% Results', 'Progress']].copy()
    display_data = display_data.sort_values(['AM', 'CUSTOMER_NAME', 'PRODUCT'])
    
    # Format columns
    display_data['NILAI'] = display_data['NILAI'].apply(format_currency)
    display_data['% Progress'] = display_data['% Progress'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "0%")
    display_data['% Results'] = display_data['% Results'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "0%")
    
    # Display dataframe
    st.dataframe(
        display_data,
        use_container_width=True,
        height=600,
        hide_index=True,
        column_config={
            "AM": st.column_config.TextColumn("Account Manager", width="medium"),
            "CUSTOMER_NAME": st.column_config.TextColumn("Customer", width="large"),
            "PRODUCT": st.column_config.TextColumn("Product", width="medium"),
            "NILAI": st.column_config.TextColumn("Nilai", width="small"),
            "% Progress": st.column_config.TextColumn("Progress", width="small"),
            "% Results": st.column_config.TextColumn("Result", width="small"),
            "Progress": st.column_config.TextColumn("Status", width="small")
        }
    )

def render_table_visualization(df, selected_witel):
    """Main function untuk render section Progress Account Manager"""
    
    # Initialize session state
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = 'card'
    
    # Header dengan toggle
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%); 
                    padding: 28px 32px; border-radius: 20px; 
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); 
                    border: 1px solid #e5e7eb;'>
            <div style='display: flex; align-items: center; gap: 16px;'>
                <div style='background: linear-gradient(135deg, #ea1d25 0%, #d61921 100%); 
                            width: 56px; height: 56px; border-radius: 14px;
                            display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 4px 16px rgba(234, 29, 37, 0.3);'>
                    <span style='font-size: 28px;'>👥</span>
                </div>
                <div>
                    <h2 style='color: #1a202c; margin: 0; font-size: 1.875rem; 
                               font-weight: 900; letter-spacing: -0.02em;'>
                        Progress Account Manager
                    </h2>
                    <p style='color: #6b7280; margin: 6px 0 0 0; font-size: 0.9375rem; 
                             font-weight: 500;'>
                        Monitoring detail progress · <b style='color: #ea1d25;'>{selected_witel}</b>
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%); 
                    padding: 20px 24px; border-radius: 20px; 
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); 
                    border: 1px solid #e5e7eb; height: 100%;
                    display: flex; flex-direction: column; justify-content: center;'>
            <div style='text-align: center; margin-bottom: 8px;'>
                <div style='color: #6b7280; font-size: 0.7rem; font-weight: 700; 
                           text-transform: uppercase; letter-spacing: 0.5px;'>
                    🎯 VIEW MODE
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Toggle buttons
        col_card, col_table = st.columns(2)
        
        with col_card:
            if st.button(
                "📋 Card",
                key="btn_card_view",
                use_container_width=True,
                type="primary" if st.session_state.view_mode == 'card' else "secondary"
            ):
                st.session_state.view_mode = 'card'
                st.rerun()
        
        with col_table:
            if st.button(
                "📊 Table",
                key="btn_table_view",
                use_container_width=True,
                type="primary" if st.session_state.view_mode == 'table' else "secondary"
            ):
                st.session_state.view_mode = 'table'
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Prepare data
    am_groups = df.groupby('AM').agg({
        'CUSTOMER_NAME': 'nunique',
        'PRODUCT': 'count',
        'NILAI': 'sum',
        '% Progress': 'mean'
    }).reset_index()
    
    am_groups.columns = ['AM', 'Total_Customers', 'Total_Products', 'Total_Nilai', 'Avg_Progress']
    am_groups = am_groups.sort_values('Total_Nilai', ascending=False)
    
    # Summary cards dengan gradient (tetap pakai gradient di summary)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ea1d25 0%, #c41e24 100%); 
                    padding: 24px; border-radius: 18px; 
                    box-shadow: 0 8px 24px rgba(234, 29, 37, 0.3); 
                    text-align: center; border: 2px solid rgba(255,255,255,0.1);
                    position: relative; overflow: hidden;'>
            <div style='position: absolute; top: -30px; right: -30px; 
                        width: 120px; height: 120px; background: rgba(255,255,255,0.08); 
                        border-radius: 50%;'></div>
            <div style='position: relative; z-index: 1;'>
                <div style='color: rgba(255,255,255,0.85); font-size: 0.75rem; font-weight: 700; 
                           text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>
                    Account Manager
                </div>
                <div style='color: white; font-size: 2.75rem; font-weight: 900; 
                           text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>
                    {len(am_groups)}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_customers = df['CUSTOMER_NAME'].nunique()
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                    padding: 24px; border-radius: 18px; 
                    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3); 
                    text-align: center; border: 2px solid rgba(255,255,255,0.1);
                    position: relative; overflow: hidden;'>
            <div style='position: absolute; top: -30px; right: -30px; 
                        width: 120px; height: 120px; background: rgba(255,255,255,0.08); 
                        border-radius: 50%;'></div>
            <div style='position: relative; z-index: 1;'>
                <div style='color: rgba(255,255,255,0.85); font-size: 0.75rem; font-weight: 700; 
                           text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>
                    Total Customer
                </div>
                <div style='color: white; font-size: 2.75rem; font-weight: 900; 
                           text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>
                    {total_customers}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_products = len(df)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); 
                    padding: 24px; border-radius: 18px; 
                    box-shadow: 0 8px 24px rgba(139, 92, 246, 0.3); 
                    text-align: center; border: 2px solid rgba(255,255,255,0.1);
                    position: relative; overflow: hidden;'>
            <div style='position: absolute; top: -30px; right: -30px; 
                        width: 120px; height: 120px; background: rgba(255,255,255,0.08); 
                        border-radius: 50%;'></div>
            <div style='position: relative; z-index: 1;'>
                <div style='color: rgba(255,255,255,0.85); font-size: 0.75rem; font-weight: 700; 
                           text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>
                    Total Produk
                </div>
                <div style='color: white; font-size: 2.75rem; font-weight: 900; 
                           text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>
                    {total_products}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_progress = df['% Progress'].mean()
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #10b981 0%, #047857 100%); 
                    padding: 24px; border-radius: 18px; 
                    box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3); 
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
                <div style='color: white; font-size: 2.75rem; font-weight: 900; 
                           text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>
                    {avg_progress:.1f}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Render based on view mode
    if st.session_state.view_mode == 'card':
        render_card_mode(df, am_groups)
    else:
        render_table_mode(df)