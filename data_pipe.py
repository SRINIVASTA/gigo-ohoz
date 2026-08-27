import streamlit as st
import pandas as pd
import numpy as np
import re

def adaptive_monetary_parser(raw_value):
    """
    Resilient regular expression financial parser. Cleans currency prefixes (AED/USD),
    stray letters, transaction noise, and standardizes localized float notation structures.
    """
    if pd.isnull(raw_value): return 0.0
    if isinstance(raw_value, (int, float)): return float(raw_value)
    clean_str = str(raw_value).upper().strip()
    
    # Strip operational masking noise and message character arrays
    clean_str = re.sub(r'\*\*\*\*\d+|\*\d+|\b\d{2}/\d{2}/\d{2,4}\b', '', clean_str)
    
    currency_pattern = r'(?:[A-Z]{3}|[\$€£₹]|TRX\.\s+OF|FOR|AED|USD|EUR|GBP|INR)\s*([-\d\.,]+)'
    match = re.search(currency_pattern, clean_str)
    target_text = match.group(1).strip() if match else clean_str
    
    # Automatically switch punctuation if comma is used as decimal separator
    if ',' in target_text and '.' in target_text:
        if target_text.rfind(',') > target_text.rfind('.'):
            target_text = target_text.replace('.', '').replace(',', '.')
        else:
            target_text = target_text.replace(',', '')
    elif ',' in target_text and '.' not in target_text:
        if len(target_text.split(',')) == 2: target_text = target_text.replace(',', '.')
        else: target_text = target_text.replace(',', '')
        
    target_text = re.sub(r'[^\d\.-]', '', target_text)
    try: 
        return float(target_text)
    except ValueError:
        fallback = re.search(r'([-\d,]+\.\d+)', clean_str)
        if fallback: return float(fallback.group(1).replace(',', ''))
        return 0.0

def trace_file_column_indices(columns_list):
    """Header-Agnostic Fuzzy Matcher to map any raw column layout to required fields."""
    normalized_cols = [str(c).lower().strip() for c in columns_list]
    mapping = {'date': None, 'amount': None, 'text': None, 'ref': None, 'payee': None}
    for idx, col in enumerate(normalized_cols):
        if any(tk in col for tk in ['date', 'time', 'timestamp']): mapping['date'] = idx
        elif any(tk in col for tk in ['amount', 'value', 'money', 'volume', 'parsed_amount', 'dr', 'cr', 'sms']): mapping['amount'] = idx
        elif any(tk in col for tk in ['sms', 'msg', 'description', 'narrative', 'text_line', 'memo', 'details']): mapping['text'] = idx
        elif any(tk in col for tk in ['id', 'reference', 'ref', 'trx', 'serial', 'tx']): mapping['ref'] = idx
        elif any(tk in col for tk in ['cardholder', 'payee', 'user', 'owner', 'client', 'vendor']): mapping['payee'] = idx
        
    if mapping['text'] is None:
        for idx, col in enumerate(normalized_cols):
            if any(tk in col for tk in ['sms', 'msg', 'text', 'string', 'object']):
                mapping['text'] = idx
                break
    return mapping

def clean_adib_description(text):
    """
    Isolates clean vendor names from chaotic ADIB bank message text streams.
    Transforms raw alert logs into structured accounting descriptions.
    """
    if not isinstance(text, str): return "UNCLASSIFIED LEDGER TRANSACTION"
    text_clean = text.strip()
    
    # CRITICAL HOTFIX MATCHERS FOR ADIB INTERNALS
    if any(tk in text_clean.upper() for tk in ["HAS BEEN CREATED", "THANK YOU FOR OPENING", "REQUESTING A NEW CHEQUEBOOK"]):
        return "SYSTEM ALERT NOTIFICATION"
    if "SALARY OF" in text_clean.upper() or "YOUR SALARY OF" in text_clean.upper():
        return "INTERNAL PAYROLL REMUNERATION INFLOW"
    if "PROFIT OF" in text_clean.upper():
        return "ADIB BANK INTEREST PROFIT CREDITED"
    if "ATM CASH WITHDRAWAL" in text_clean.upper():
        return "ATM VAULT LIQUID CASH DISBURSEMENT"
    if "PAYMENT FOR YOUR COVERED CARD WAS DEBITED" in text_clean.upper():
        return "INTERNAL COVERED CARD LIABILITY SETTLEMENT"
        
    # Check for flat transfer credits and debits
    if "WAS CREDITED TO YOUR ACCOUNT" in text_clean.upper() or "WAS CREDITED" in text_clean.upper():
        return "DIRECT SYSTEM CAPITAL/TRANSFER INFLOW"
    if "WAS DEBITED FROM YOUR ACCOUNT" in text_clean.upper() or "WAS DEBITED" in text_clean.upper():
        return "DIRECT ACCOUNT LIQUIDITY TRANSFER OUTFLOW"
    
    # Strip standard POS transaction prefixes to capture merchant footprints
    text_clean = re.sub(r'(?i)^Trx\.\s+of\s+[A-Z]{3}\s+[\d\.,]+\s+on\s+your\s+a/c\s+\**\d+\s+at\s+', '', text_clean)
    text_clean = re.sub(r'(?i)^Transaction\s+of\s+[A-Z]{3}\s+[\d\.,]+\s+debited\s+from\s+your\s+a/c\s+\**\d+\s+at\s+', '', text_clean)
    text_clean = re.sub(r'(?i)^Trx\.\s+of\s+[A-Z]{3}\s*[\d\.,]+\s+on\s+your\s+card\s+ending\s+\**\d+\s+at\s+', '', text_clean)
    text_clean = re.sub(r'(?i)^A\s+POS\s+Trxn\s+on\s+your\s+Account\s+No\s+\**\d+\s+at\s+', '', text_clean)
    text_clean = re.sub(r'(?i)^Trx\.\s+of\s+[A-Z]{3}\s*[\d\.,]+\s+on\s+your\s+card\s+ending\s+\**\d+\s+at\s+', '', text_clean)

    # Strip localized bank terminal operational suffixes
    split_patterns = r'(?i)\.\s*Avl|\.\s*Your|\.Your|\s+on\s+\d{2}/\d{2}/\d{2,4}|\s+in\s+[A-Z]{2,3}\s+on|\s+is\s+Approved'
    parts = re.split(split_patterns, text_clean)
    text_clean = parts[0]
        
    return text_clean.strip().upper()

def generic_zoho_pipeline_classifier(sms_narrative, numeric_valuation):
    """Universal classification router with deep tax jurisdiction lookup."""
    if pd.isnull(sms_narrative) or str(sms_narrative).strip() == "":
        return "⚠️ Suspense Profile", "4999", "UNCLASSIFIED ROW", 0.0, "Exempt"
    text = str(sms_narrative).upper()
    val = float(numeric_valuation)
    
    secrets_titles = st.secrets.get("group_titles", {})
    secrets_lexicon = st.secrets.get("universal_lexicon", {})
    tax_rules = st.secrets.get("tax_jurisdictions", {})

    # Inward/Outward default fallbacks
    account_code = "4999"
    
    if "SYSTEM ALERT" in text or "SECURITY CODE" in text:
        return "⚠️ System Alert Profile", "9999", "SYSTEM ALERT MATRIX", 0.0, "Exempt"
        
    # Catch Cleaned Internal Sorters instantly
    if "PAYROLL" in text or "REMUNERATION" in text:
        account_code = "2000"
    elif "INTEREST" in text or "PROFIT CREDITED" in text:
        account_code = "2100"
    elif "ATM" in text or "LIQUID CASH" in text:
        account_code = "1000"
    elif "LIQUIDITY TRANSFER" in text or "CAPITAL/TRANSFER" in text or "LIABILITY SETTLEMENT" in text:
        account_code = "1050"
    else:
        # Evaluate against token catalog
        matched = False
        for code, patterns in secrets_lexicon.items():
            if any(str(pattern).upper() in text for pattern in patterns):
                account_code = str(code)
                matched = True
                break
            if matched: break

    group_info = secrets_titles.get(account_code, "Mapped Account")
    tax_rate = float(tax_rules.get(f"{account_code}_rate", 0.0))
    tax_name = tax_rules.get(f"{account_code}_name", "Zero Rated (0%)")

    return group_info, account_code, group_info, tax_rate, tax_name

def assemble_universal_audit_trail(df):
    """Calculates comprehensive tax-inclusive ledger receipts vs disbursements balance matrices."""
    inflows = df[df['Signed_Amount'] > 0]['Signed_Amount'].sum()
    outflows = df[df['Signed_Amount'] < 0]['Signed_Amount'].sum()
    net_bal = df['Signed_Amount'].sum()
    total_tax_collected = df['Tax Amount'].sum()
    
    secrets_titles = st.secrets.get("group_titles", {})
    audit_rows = []
    for code, metadata in secrets_titles.items():
        code_sum = df[df['Zoho_Account_Code'] == code]['Signed_Amount'].sum()
        audit_rows.append([f"Account {code} Balance ({metadata})", code_sum, metadata])
        
    audit_rows.extend([
        ["Total Receipts Volume (+)", inflows, "Gross Inbound Velocity Summary"],
        ["Total Disbursements Volume (-)", outflows, "Gross Outbound Velocity Summary"],
        ["Aggregated Extracted Tax Throughput", total_tax_collected, "Tax Extraction Check"],
        ["Statement General Ledger Net Balance Check", net_bal, "Financial Baseline Check"]
    ])
    
    recon_df = pd.DataFrame(audit_rows, columns=["Audit Ledger Evaluation Metric", "Aggregated Balance", "Meta Classification Group"])
    
    working_df = df.copy()
    working_df['Abs_Val'] = working_df['Signed_Amount'].abs()
    working_df['Receipts_Volume'] = np.where(working_df['Signed_Amount'] > 0, working_df['Signed_Amount'], 0)
    working_df['Expenditures_Volume'] = np.where(working_df['Signed_Amount'] < 0, working_df['Abs_Val'], 0)
    
    global_matrix = working_df.groupby('Zoho_Account_Code').agg(
        Net_Balance=('Signed_Amount', 'sum'),
        Inbound_Receipts_Volume=('Receipts_Volume', 'sum'),
        Outbound_Expenditures_Volume=('Expenditures_Volume', 'sum'),
        Extracted_Tax_Volume=('Tax Amount', 'sum'),
        Total_Row_Count=('Zoho_Account_Code', 'count')
    ).reset_index()
    
    global_matrix['Ledger Category Title Sorter Name'] = global_matrix['Zoho_Account_Code'].map(
        lambda x: secrets_titles.get(str(x), "Unmapped Baseline Account Profile")
    )
    
    total_volume_throughput = global_matrix['Inbound_Receipts_Volume'].sum() + global_matrix['Outbound_Expenditures_Volume'].sum()
    global_matrix['Global Ledger Activity Weight (%)'] = (
        ((global_matrix['Inbound_Receipts_Volume'] + global_matrix['Outbound_Expenditures_Volume']) / total_volume_throughput) * 100
    ).round(2) if total_volume_throughput > 0 else 0
    
    global_matrix = global_matrix[[
        'Zoho_Account_Code', 'Ledger Category Title Sorter Name', 
        'Net_Balance', 'Inbound_Receipts_Volume', 'Outbound_Expenditures_Volume', 'Extracted_Tax_Volume',
        'Total_Row_Count', 'Global Ledger Activity Weight (%)'
    ]].sort_values(by='Total_Row_Count', ascending=False)
    
    return recon_df, global_matrix

def execute_universal_etl_pipeline(raw_df):
    """Parses dynamic columns, extracts global sales tax allocations, and configures Zoho sheets."""
    col_map = trace_file_column_indices(raw_df.columns)
    processed_df = pd.DataFrame()
    
    if col_map['date'] is not None:
        processed_df['Transaction Date'] = pd.to_datetime(raw_df.iloc[:, col_map['date']]).dt.strftime('%Y-%m-%d')
    else:
        processed_df['Transaction Date'] = pd.Timestamp.now().strftime('%Y-%m-%d')
        
    raw_text_idx = col_map['text'] if col_map['text'] is not None else (col_map['amount'] if col_map['amount'] is not None else 0)
    raw_text_series = raw_df.iloc[:, raw_text_idx].astype(str)
    
    processed_df['Raw_Description'] = raw_text_series.fillna("Empty Ledger Line Log")
    processed_df['Description'] = processed_df['Raw_Description'].apply(clean_adib_description)
    
    if col_map['amount'] is not None:
        processed_df['Signed_Amount'] = raw_df.iloc[:, col_map['amount']].apply(adaptive_monetary_parser)
    else:
        processed_df['Signed_Amount'] = processed_df['Raw_Description'].apply(adaptive_monetary_parser)
        
    deduction_triggers = ["debited", "withdrawal", "payment for", "trx. of", "transaction of"]
    processed_df['Signed_Amount'] = np.where(
        processed_df['Raw_Description'].str.contains('|'.join(deduction_triggers), case=False, na=False) & 
        (~processed_df['Raw_Description'].str.contains("reversed|refund", case=False, na=False)),
        -processed_df['Signed_Amount'].abs(),
        processed_df['Signed_Amount'].abs()
    )
    
    processed_df['Reference Number'] = raw_df.iloc[:, col_map['ref']] if col_map['ref'] is not None else ""
    processed_df['Payee/Vendor'] = raw_df.iloc[:, col_map['payee']] if col_map['payee'] is not None else "Global Ledger Account"
    
    # 🏁 UNPACKING TUPLE UNIFIED PASSTHROUGH FIX
    classification_results = [
        generic_zoho_pipeline_classifier(row['Description'], row['Signed_Amount']) 
        for _, row in processed_df.iterrows()
    ]
    
    # Safely unpack individual array indices from classification results tuple
    processed_df['Zoho_Account_Code'] = [r[1] for r in classification_results]
    processed_df['Tax Rate'] = [float(r[3]) for r in classification_results] # 🛠️ CRITICAL HOTFIX: Forced Type Casting to Float
    processed_df['Tax Name'] = [r[4] for r in classification_results]
    
    processed_df['Absolute_Gross'] = processed_df['Signed_Amount'].abs()
    processed_df['Net Amount'] = (processed_df['Absolute_Gross'] / (1.0 + processed_df['Tax Rate'])).round(2)
    processed_df['Tax Amount'] = (processed_df['Absolute_Gross'] - processed_df['Net Amount']).round(2)
    
    processed_df['Debit (Payments)'] = np.where(processed_df['Signed_Amount'] < 0, processed_df['Absolute_Gross'], 0.0)
    processed_df['Credit (Deposits)'] = np.where(processed_df['Signed_Amount'] > 0, processed_df['Absolute_Gross'], 0.0)
    
    processed_df = processed_df[processed_df['Zoho_Account_Code'] != '9999']
    
    recon_df, global_dist_df = assemble_universal_audit_trail(processed_df)
    
    final_zoho_df = processed_df[[
        'Transaction Date', 'Description', 'Debit (Payments)', 'Credit (Deposits)', 
        'Net Amount', 'Tax Amount', 'Tax Name', 'Reference Number', 'Zoho_Account_Code', 'Payee/Vendor'
    ]]
    
    return final_zoho_df, recon_df, global_dist_df, col_map, processed_df['Signed_Amount']
