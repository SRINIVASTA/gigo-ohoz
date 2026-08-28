# 📊 gigo-ohoz | Universal Zoho Books Ingestion Portal

An enterprise-grade, country-adaptive **automated financial ingestion dashboard & ETL engine** built specifically for Zoho Books imports. 

By subverting the traditional **GIGO (Garbage In, Garbage Out)** paradigm, this platform intercepts chaotic, poorly formatted data packets (Garbage In), normalizes structural noise, handles variable token maps dynamically on the fly, and outputs a pristine, transaction-level vector upload package (Purified Out) mapped directly to your financial specifications.

---
## 🔒 Zero Data Saving Architecture (Transient In-Memory ETL)

To ensure strict compliance with global corporate financial privacy mandates, this portal enforces a strict **Zero Data Saving (Stateless)** execution profile:

* **Pure RAM Processing:** Uploaded files ingested via `st.file_uploader` are held strictly within transient memory (RAM) buffer arrays.
* **No Disk Tracking:** The backend ETL engine (`data_pipe.py`) performs all normalization, token extractions, and split-vector calculations entirely in-memory. No raw data, logs, or intermediate spreadsheet rows are ever written to local server disk storage.
* **Instant Session Purge:** The moment a user closes or refreshes their browser viewport tab, all transaction matrices are immediately wiped out of the active runtime state. 
* **Zero Asset Persistence:** Because no persistent files are ever generated on the server side, a root `.gitignore` file for data protection is completely non-required for cloud deployment.

---

## 📈 System Architecture

The project utilizes a decoupled, split-architecture design to isolate tax-aware core calculation data models from presentation layouts:

```text
📁 gigo-ohoz/
│
├── 📄 app.py                     # Front-end workspace UI viewport presentation layer
├── 📄 data_pipe.py               # Back-end Zoho vector splitter & tax calculation engine
├── 📄 README.md                  # System operation & architectural documentation
└── 📄 requirements.txt           # Explicit python dependency manifest file
```

---

## ✨ Core Features

* **Double Footprint Accounting Audits:** The dashboard tracks and cross-references **Total Raw Rows** directly against **Cleaned Mapped Transactions**, exposing the exact line-item delta skipped during data parsing.
* **Text-to-Column Extraction Engine:** Strips out unformatted bank conversational SMS notification messages and extracts clean data parameters into structured relational tables (separating Date, Amount, Type, and Merchant).
* **Zoho Absolute Vector Splitting:** Automatically maps out signed positive and negative records, sorting them into separate, explicit `Debit (Payments)` and `Credit (Deposits)` absolute column fields to comply with native Zoho Books banking template guidelines.
* **Jurisdiction-Aware Tax Splitter:** Evaluates mathematical base scaling algorithms to back out internal fractional tax weights: `Net Amount = Gross / (1 + Rate)`.
* **Zero-Accounting Fallback Filters:** Automatically segregates non-monetary system logs (like bank OTP strings, service notifications, or welcome greetings) into a temporary workspace holding pool.
* **Cryptographic Firewall Perimeter:** Enforces a secure, state-managed authentication token gateway that blocks underlying application execution until a valid token string is verified.

---

## 🗂️ Live Statement Operation Panel Sorter

The engine separates your workflow into four layouts. **Panel 1 provides your primary upload vector**, while **Panels 2 through 4 are provided strictly for user viewing, local data auditing, and manual verification purposes**:

### 1. 🟢 Zoho Books Import Layout (`.csv` / `.xlsx`) 
* **Zoho Ingestion Route:** `Banking -> Import Statement`
* **Execution Status:** **REQUIRED FOR UPLOAD.**
* **GIGO Ingestion Mode:** **Data Output Vector.** 
* **Description:** This is the *only* file uploaded to Zoho Books. It contains a flat, row-by-row matrix of individual financial entries. All raw text message clutter is removed.
* **Ingestion Parameter Mapping:**
  * `Transaction Date` ➡️ Transaction Date
  * `Description` ➡️ Description
  * `Debit (Payments)` ➡️ Withdrawals / Expense
  * `Credit (Deposits)` ➡️ Deposits / Income
  * `Reference Number` ➡️ Reference Number
  * *Note: Extra reference fields such as `Zoho_Account_Code` and `Tax Name` are completely skipped and ignored by the database engine on upload.*

### 2. ❌ Balance Verification Audit
* **Zoho Ingestion Route:** *None (Keep Local Workspace View)*
* **Execution Status:** **USER VIEWING ONLY (DO NOT UPLOAD).**
* **GIGO Ingestion Mode:** **Audit Verification Pass.**
* **Description:** An interactive dashboard view tracking cumulative net financial balance checks (e.g., target balance changes). It is provided strictly for you to view and check calculations against your banking portal totals before pushing entries into Zoho.

### 3. ❌ Global Ledger Spend & Activity Sorter
* **Zoho Ingestion Route:** *None (Keep Local Workspace View)*
* **Execution Status:** **USER VIEWING ONLY (DO NOT UPLOAD).**
* **GIGO Ingestion Mode:** **Analytical Sorter View.**
* **Description:** Provides a management overview report tracking percentage weights across ledger accounts. It serves as an interactive data filter tool for you to review spend allocations and spot high-volume activity buckets.

### 4. ❌ Advanced Ingestion Metadata Mapping Logs
* **Zoho Ingestion Route:** *None (Keep Local Workspace View)*
* **Execution Status:** **USER VIEWING ONLY (DO NOT UPLOAD).**
* **GIGO Ingestion Mode:** **ETL Pipeline Map.**
* **Description:** A live script execution map displaying exactly where headers and token arrays (`date`, `amount`, `text`, `ref`, `payee`) were located inside your raw sheet. It is provided for your reference to verify data-line lineage without cluttering Zoho Books.

---

## 🚀 Quick Start Deployment Execution

1. Initialize your localized repository workspace environment:
   ```bash
   git init gigo-ohoz
   cd gigo-ohoz
   ```
2. Setup and install required package bins using your terminal session execution panel:
   ```bash
   pip install -r requirements.txt
   ```
3. Boot up the Streamlit engine processing server instance:
   ```bash
   streamlit run app.py
   ```

---

## 🛡️ Cloud-Native Security Design

* **De-coupled Architecture:** Core backend calculation logic files are fully isolated from presentation viewport layouts to secure internal account parsing parameters from style adjustments.
* **Exclusion Control Mandate:** Local storage verification sheets, raw text data spreadsheets, and testing environment files must be stringently blocked within the root `.gitignore` configuration tracking file to prevent leaks.
