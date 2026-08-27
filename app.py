import streamlit as st

# ==============================================================================
# 1. INITIAL POSITION PAGE SPECIFICATIONS (MUST BE EXECUTED FIRST)
# ==============================================================================
st.set_page_config(
    page_title="GIGO-OHOZ | Universal Zoho Books Ingestion Portal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import numpy as np
import re
import io
import plotly.express as px
import logging
from data_pipe import execute_universal_etl_pipeline

# ==============================================================================
# 2. FORCE STREAMLIT CHROMIUM HIDING LAYERS & GAP FIX
# ==============================================================================
st.markdown(""" 
 <style> 
 header[data-testid="stHeader"] { visibility: hidden !important; display: none !important; } 
 div[data-testid="stToolbar"] { visibility: hidden !important; display: none !important; } 
 footer { visibility: hidden !important; } 
 
 [data-testid="stMainBlockContainer"] { padding-top: 1rem !important; }
 .main .block-container { padding-top: 1rem !important; }
 div[data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #0066cc; }
 div[data-testid="stMetricLabel"] { font-size: 14px; color: #4B5563; text-transform: uppercase; letter-spacing: 0.5px; }
 h1 { color: #0066cc; font-weight: 800; }
 </style> 
 """, unsafe_allow_html=True) 

logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger("FIREWALL") 

def verify_and_log_locally(user_key): 
    try:
        valid_keys = st.secrets["APPROVED_LICENSE_KEYS"]
    except Exception:
        st.error("🚨 CONFIGURATION ERROR: 'APPROVED_LICENSE_KEYS' list not found in cloud secrets.")
        return False, None, "AED", "Standard Tax"

    if user_key not in valid_keys: 
        logger.error("🔴 REJECTED: Invalid key structure submitted.") 
        return False, None, "AED", "Standard Tax"
        
    detected_country = "Global Operations Gateway"
    currency_symbol = "AED"
    tax_label = "VAT"
    
    if "-IN-" in user_key:
        detected_country = "India Tax Jurisdiction"
        currency_symbol = "INR"
        tax_label = "GST"
    elif "-US-" in user_key:
        detected_country = "United States Jurisdiction"
        currency_symbol = "USD"
        tax_label = "Sales Tax"
    elif "-UK-" in user_key or "-GB-" in user_key:
        detected_country = "United Kingdom Jurisdiction"
        currency_symbol = "GBP"
        tax_label = "UK VAT"
        
    logger.info(f"✅ ACCESS GRANTED: Profile matched for context: {detected_country}") 
    return True, f"{detected_country} (Cloud Verified)", currency_symbol, tax_label

# State Management Initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "detected_location" not in st.session_state:
    st.session_state.detected_location = None
if "currency" not in st.session_state:
    st.session_state.currency = "AED"
if "tax_label" not in st.session_state:
    st.session_state.tax_label = "VAT"

st.sidebar.title("🔑 Software Security Portal") 

if not st.session_state.authenticated:
    license_input = st.sidebar.text_input("Enter License Key:", type="password") 
    if st.sidebar.button("Validate License Key", use_container_width=True):
        if license_input:
            is_valid, loc, cur, tax_lbl = verify_and_log_locally(license_input)
            if is_valid:
                st.session_state.authenticated = True
                st.session_state.detected_location = loc
                st.session_state.currency = cur
                st.session_state.tax_label = tax_lbl
                st.rerun()
            else:
                st.sidebar.error("🚨 ACCESS DENIED: Invalid or Unpaid Software License Key.")
        else:
            st.sidebar.warning("Please provide a licensing token configuration value.")
else:
    st.sidebar.success(f"🔒 Active Framework: {st.session_state.detected_location}")
    if st.sidebar.button("Log Out / Lock Console", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.detected_location = None
        st.rerun()

if not st.session_state.authenticated:
    st.title("🔒 GIGO-OHOZ | Ingestion & Tax Extraction Engine")
    st.warning("### **Access Unauthorized**")
    st.markdown("This database conversion tool is protected by localized country accounting wrappers. Enter a valid software authorization key in the left Control Console sidebar to switch into regional mode.")
    st.stop()
# ==============================================================================
# 3. CONTROL CONSOLE WORKSPACE LAYER (RUNS ONLY WHEN AUTHENTICATED)
# ==============================================================================
with st.sidebar:
    st.markdown("## **Control Console**")
    st.markdown(f"Processing local bank feeds format structure cleanly to **Zoho Books** standards under **{st.session_state.tax_label}** parameters.")
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "⚡ Ingest Transaction Profile File", 
        type=["csv", "xlsx", "xls", "txt"],
        help="Supports generic banking rows, SMS sheets, or standard statement data."
    )
    st.markdown("---")
    st.markdown("### **System Status**")
    if uploaded_file is not None:
        st.info("🟢 File loaded successfully. Ready for processing pass.")
    else:
        st.warning("⚠️ Awaiting financial source file upload wrapper...")

if uploaded_file is None:
    st.title(f"📊 Zoho Books Financial Data Ingestion Dashboard ({st.session_state.currency})")
    st.markdown("Welcome to the dynamic Zoho accounting ledger pipeline suite. Upload raw files to clear text noise, map accounting codes, and compute automated localized tax breakdowns on the fly.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("#### ⚙️ In-Country Processing Features\n"
                "* **Fuzzy Field Matcher:** Maps messy bank data layouts seamlessly.\n"
                "* **Tax Splitter Engine:** Automatically extracts tax elements from composite totals based on chart configurations.\n"
                "* **Zoho Vector Balancer:** Splits signed positive/negative structures into scalar payments and deposits fields.")
    with col2:
        st.info("#### 🛡️ Cloud-Native Security Design\n"
                "* **Isolated Logic Architecture:** Script calculation structures are segregated from presentation modules.\n"
                "* **Encrypted Secrets Allocation:** Mapping dictionaries are securely isolated out of source control footprints.")
else:
    file_name = uploaded_file.name
    file_ext = re.sub(r'.*(\..*)$', r'\1', file_name).lower()
    raw_input_df = None
    
    try:
        if file_ext in ['.xlsx', '.xls']:
            excel_file_object = pd.ExcelFile(uploaded_file)
            sheet_names_list = excel_file_object.sheet_names
            if len(sheet_names_list) > 1:
                selected_sheet = st.sidebar.selectbox("📁 Target Sheet Selection Panel:", options=sheet_names_list)
                raw_input_df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
            else:
                raw_input_df = pd.read_excel(uploaded_file, sheet_name=0)
        elif file_ext == '.csv':
            raw_input_df = pd.read_csv(uploaded_file)
        else:
            raw_input_df = pd.read_csv(uploaded_file, sep=None, engine='python')
    except Exception as e:
        st.error(f"Critical Ingestion Error: {e}")
        raw_input_df = None

    if raw_input_df is not None:
        final_zoho_df, reconciliation_df, global_distribution_df, dynamic_layout_indices, signed_amounts_series = execute_universal_etl_pipeline(raw_input_df)
        
        grand_total_rows = int(global_distribution_df["Total_Row_Count"].sum())
        total_activity_weight = global_distribution_df["Global Ledger Activity Weight (%)"].sum()
        
        totals_row = pd.DataFrame([{
            'Zoho_Account_Code': 'TOTALS',
            'Ledger Category Title Sorter Name': 'Grand Total Summary Slices',
            'Net_Balance': signed_amounts_series.sum(),
            'Inbound_Receipts_Volume': global_distribution_df['Inbound_Receipts_Volume'].sum(),
            'Outbound_Expenditures_Volume': global_distribution_df['Outbound_Expenditures_Volume'].sum(),
            'Extracted_Tax_Volume': global_distribution_df['Extracted_Tax_Volume'].sum(),
            'Total_Row_Count': grand_total_rows,
            'Global Ledger Activity Weight (%)': round(total_activity_weight, 2)
        }])
        
        display_distribution_df = pd.concat([global_distribution_df, totals_row], ignore_index=True)

        st.title(f"📊 Zoho Books Audit & Ingestion Workspace ({st.session_state.currency})")
        st.markdown(f"Currently analyzing worksheet data matrix. Ingested profile table footprint contains **{grand_total_rows:,} records**.")

        st.markdown(f"### 📋 GENERAL LEDGER PERFORMANCE RECONCILIATION CARDS ({st.session_state.currency})")
        kpi_container = st.container()
        with kpi_container:
            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
            with kpi_col1:
                st.metric(label="✨ Grand Sum Row Footprint", value=f"{grand_total_rows:,} Transactions")
            with kpi_col2:
                st.metric(label="💰 Statement Net Cash-Flow", value=f"{st.session_state.currency} {signed_amounts_series.sum():,.2f}")
            with kpi_col3:
                st.metric(label="🧾 Extracted Tax Summary", value=f"{st.session_state.currency} {final_zoho_df['Tax Amount'].sum():,.2f}")
            with kpi_col4:
                unmapped_rows = int(global_distribution_df[global_distribution_df['Zoho_Account_Code'] == '4999']['Total_Row_Count'].sum())
                st.metric(label="⚠️ Unmapped Fallbacks", value=f"{unmapped_rows} Rows")

        st.markdown("---")
        # ==============================================================================
        # 4. DATA VISUALIZATION LAYER (HIGH-IMPACT INTERACTIVE DESKTOP CHARTS)
        # ==============================================================================
        st.markdown("### 📊 INTERACTIVE SPEND WEIGHTS & ACTIVITY DISPERSION LOGS")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            spend_chart_df = global_distribution_df[global_distribution_df['Outbound_Expenditures_Volume'] > 0].copy()
            if not spend_chart_df.empty:
                fig_spend = px.bar(
                    spend_chart_df,
                    x='Outbound_Expenditures_Volume',
                    y='Ledger Category Title Sorter Name',
                    orientation='h',
                    title='Total Outbound Spend Dispersal by Zoho Account Group',
                    labels={'Outbound_Expenditures_Volume': f'Total Value ({st.session_state.currency})', 'Ledger Category Title Sorter Name': 'Account Category'},
                    color='Outbound_Expenditures_Volume',
                    color_continuous_scale='Blues',
                    template='plotly_white'
                )
                fig_spend.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False, height=350, margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_spend, use_container_width=True)
            else:
                st.info("No outbound general ledger expense records available to render charts.")

        with chart_col2:
            fig_pie = px.pie(
                global_distribution_df,
                values='Total_Row_Count',
                names='Zoho_Account_Code',
                title='Zoho Chart Activity Row Concentration (%)',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Blues_r,
                template='plotly_white'
            )
            fig_pie.update_layout(height=350, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("---")

        # ==============================================================================
        # 5. DATA GRIDS LAYOUT RECONCILIATION TABS
        # ==============================================================================
        st.subheader("📋 GENERAL LEDGER VERIFICATION SHEETS & IMPORT GENERATION AUDIT")
        tab1, tab2, tab3 = st.tabs([f"Zoho Books Import Layout ({st.session_state.tax_label})", "Balance Verification Audit", "Global Ledger Spend & Activity Sorter"])
        
        with tab1:
            st.markdown(f"##### Cleaned bank import formatting structure with localized tax codes mapped to Zoho Books upload specifications.")
            st.dataframe(final_zoho_df, use_container_width=True, height=300)
        with tab2:
            st.markdown("##### Pre-import generalization scorecard analysis balancing inflow gross velocities vs outflows.")
            st.dataframe(reconciliation_df, use_container_width=True, height=300)
            
        with tab3:
            st.markdown("##### Global activity summary matrix. Select any row checkbox to instantly load specific account entries underneath.")
            clicked_event = st.dataframe(
                display_distribution_df,
                use_container_width=True,
                height=300,
                on_select="rerun",
                selection_mode="multi-row"
            )
            
            selected_row_indices = clicked_event.get("selection", {}).get("rows", [])
            if len(selected_row_indices) > 0:
                target_row_index = int(selected_row_indices[0])
                clicked_code = display_distribution_df.iloc[target_row_index]['Zoho_Account_Code']
                
                if pd.notnull(clicked_code) and clicked_code != 'TOTALS':
                    secrets_titles = st.secrets.get("group_titles", {})
                    st.markdown(f"### 🎯 Underlying Transactions Sorter Preview for Account `[{clicked_code}] - {secrets_titles.get(clicked_code, 'Base Account')}`")
                    
                    tgt_logs_df = final_zoho_df[final_zoho_df['Zoho_Account_Code'] == clicked_code]
                    
                    sub_col1, sub_col2, sub_col3 = st.columns(3)
                    with sub_col1:
                        st.markdown(f"**Total Payments Volume (Debit):** `{st.session_state.currency} {tgt_logs_df['Debit (Payments)'].sum():,.2f}`")
                    with sub_col2:
                        st.markdown(f"**Total Net Base Volume:** `{st.session_state.currency} {tgt_logs_df['Net Amount'].sum():,.2f}` | **Tax Allocation:** `{st.session_state.currency} {tgt_logs_df['Tax Amount'].sum():,.2f}`")
                    with sub_col3:
                        st.markdown(f"**Total Entry Rows Density:** `{len(tgt_logs_df)} Rows`")
                        
                    st.dataframe(tgt_logs_df, use_container_width=True, height=200)
            
        buffer_memory_stream = io.BytesIO()
        with pd.ExcelWriter(buffer_memory_stream, engine='xlsxwriter') as workbook_writer:
            final_zoho_df.to_excel(workbook_writer, sheet_name='Zoho Books Import layout', index=False)
            reconciliation_df.to_excel(workbook_writer, sheet_name='Balance Verification Audit', index=False)
            global_distribution_df.to_excel(workbook_writer, sheet_name='Global Activity Sorter', index=False)
            
        st.markdown("---")
        st.download_button(
            label=f"💾 Download Compiled Multi-Tab Zoho Reporting Package ({st.session_state.currency})",
            data=buffer_memory_stream.getvalue(),
            file_name=f"Universal_Zoho_Purified_{st.session_state.currency}_Package.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
        with st.expander("🛠️ Advanced Ingestion Metadata Mapping Logs", expanded=False):
            st.json({k: (f"Detected at column index [{v}] ({raw_input_df.columns[v]})" if v is not None else "Missing - Using Fallback Parsing Engine") for k, v in dynamic_layout_indices.items()})
