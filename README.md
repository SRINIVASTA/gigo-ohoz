# 📊 gigo-ohoz | Universal Zoho Books Ingestion Portal

An enterprise-grade, country-adaptive **automated financial ingestion dashboard & ETL engine** built specifically for Zoho Books. 

By subverting the traditional **GIGO (Garbage In, Garbage Out)** paradigm, this platform ingests chaotic, poorly formatted bank transaction logs and SMS data packets, automatically standardizes currency/decimal notations, extracts hidden tax bases, and outputs a pristine `.xlsx` upload package mapped directly to Zoho's split-vector specifications.

---

## 📈 System Architecture

The project utilizes a decoupled, split-architecture design to isolate tax-aware core logic from presentation layouts:

```text
📁 gigo-ohoz/
│
├── 📄 .gitignore                 # Strict data & secrets exclusion ruleset
├── 📄 app.py                     # Front-end workspace UI viewport presentation layer
├── 📄 data_pipe.py               # Back-end Zoho vector splitter & tax calculation engine
└── 📄 requirements.txt           # Explicit python dependency manifest file
```

---

## ✨ Core Features

* **Double Footprint Accounting Audits:** Your KPI dashboard explicitly tracks and cross-references **Total Raw Excel Rows** directly against your **Cleaned Mapped Transactions**, exposing the precise line-item delta skipped during cleanup filters.
* **Header-Agnostic Fuzzy Parsing:** Intelligently maps column positions dynamically, targeting variable keys like `Date`, `SMS text lines`, and `Amount` configurations without template structural lock-ins.
* **Resilient Monetary Normalization:** Strips text noise, localized letters, currency prefixes (`AED`, `INR`, `USD`), and sanitizes European punctuation markings on the fly.
* **Zoho Absolute Vector Splitting:** Converts signed positive/negative items instantly into split absolute payments and deposits scalars to fulfill native Zoho template guidelines.
* **Jurisdiction-Aware Tax Splitter:** Reads fractional rates from secure metadata keys, backed out internally using mathematical base scaling algorithms: `Net = Gross / (1 + Rate)`.
* **Cryptographic Firewall Perimeter:** Enforces a severe, state-managed authentication token wrapper gate that immediately blocks underlying logic compilation until a valid token string is verified.

---
---

## 🚀 Quick Start Deployment Execution

1. Initialize your localized repository workspace environment:
   ```bash
   git init gigo-ohoz
   cd gigo-ohoz
   ```
2. Setup and install package bins using your terminal session execution panel:
   ```bash
   pip install -r requirements.txt
   ```
3. Boot up the Streamlit processing server instance:
   ```bash
   streamlit run app.py
   ```
4. Access your secure ingestion viewport panel on your native local desktop desktop (`http://localhost:8501`).

---

## 🛡️ Cloud-Native Security Design

* **De-coupled Architecture:** UI code layouts are isolated entirely from structural accounting models to safeguard calculation arrays from style block refactors.
* **Exclusion Control Mandate:** Local storage verification sheets, raw text data spreadsheets, and cloud configurations files must be stringently blocked within the root `.gitignore` tracking schema parameters.
