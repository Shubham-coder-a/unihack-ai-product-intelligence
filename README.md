# ⚡ AI Product Intelligence Platform
### Industrial Commerce Product Data Enrichment & Quality Audit Engine
**UniHack 2026 Prototype**

---

## 📌 Project Overview
The **AI Product Intelligence Platform** is an enterprise-ready prototype designed to transform unstructured, incomplete, and noisy industrial product data into structured, commerce-ready catalog records. Built with **Streamlit** and powered by **Groq Llama-3.3 70B**, the platform normalizes technical specifications, standardizes product taxonomy (UNSPSC), and provides real-time data quality audit scoring.

---

## 🚨 Problem Statement
Industrial e-commerce distributors and manufacturers manage thousands of SKUs from hundreds of suppliers. Common challenges include:
- **Missing & Inconsistent Attributes**: Unstructured titles, missing brand names, or missing technical specs.
- **Supplier Data Fragmentation**: Different suppliers format attributes differently (e.g. `1/2"`, `0.5 in`, `12.7mm`).
- **Low Conversion & Poor Searchability**: Incomplete product listings reduce customer trust and prevent effective catalog search and filtering.
- **Manual Data Cleaning Bottlenecks**: Manual enrichment takes weeks of engineering labor per vendor catalog.

---

## 💡 Solution
Our platform automates industrial data enrichment using LLM-driven intelligence:
1. **Automated Title & Description Standardizer**: Converts raw strings into standard B2B commerce titles and short descriptions.
2. **Technical Specification Extractor**: Extracts normalized key-value pairs (e.g., `Material: 316 Stainless Steel`, `Pressure Rating: 1000 PSI`).
3. **UNSPSC Taxonomy Mapper**: Automatically assigns standard commodity categories and 8-digit UNSPSC codes.
4. **Data Quality Audit Engine**: Quantifies data completeness uplift (Pre vs Post completeness %) and assigns letter grades (`A+` to `F`).
5. **Interactive UI & Export Hub**: Allows side-by-side inspection and multi-format exports (CSV, JSON).

---

## ✨ Key Features

- **📥 Dual Dataset Ingestion**: Supports `.csv` and `.xlsx` uploads plus a 1-click sample industrial catalog loader.
- **⚙️ Dynamic AI Controls**: Sidebar options for selecting Groq LLM architectures (`Llama 3.3 70B`, `Llama 3.1 8B`, `Mixtral 8x7b`) and configurable batch processing limits.
- **📊 Real-Time Quality Dashboard**: Live KPI cards showing Pre-Enrichment Completeness %, Post-Enrichment Completeness %, Completeness Uplift %, and Quality Grade.
- **🔍 Interactive Side-by-Side Explorer**: Inspect raw catalog JSON alongside AI-enriched product cards and specification tables.
- **⬇️ Dual Export Hub**: One-click exports in CSV and JSON formats for e-commerce, PIM, and search indexing integration.

---

## 🏗️ Architecture & Project Structure

```
unihack-ai-product-intelligence/
│
├── app/
│   └── app.py                  # Streamlit dashboard interface & interactive tabs
│
├── src/
│   ├── __init__.py             # Package initializer
│   ├── config.py               # Environment configuration & Groq model settings
│   ├── schemas.py              # Pydantic schemas for EnrichedProduct & DataQualityAudit
│   ├── enricher.py             # Groq LLM client wrapper & resilient JSON cleaner
│   ├── quality.py              # Data Quality & Completeness Audit engine
│   └── samples.py              # Sample dataset loader helper
│
├── data/
│   └── sample_industrial_products.csv # Realistic industrial product dataset
│
├── tests/
│   ├── test_enricher.py        # Unit tests for JSON cleaner and prompt construction
│   └── test_quality.py         # Unit tests for completeness scoring and audit reports
│
├── .env                        # Environment variables (GROQ_API_KEY)
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
└── README.md                   # Complete documentation
```

---

## 🛠️ Technologies Used

- **Python 3.10+**: Core programming language.
- **Streamlit**: Web application framework.
- **Groq API**: Ultra-fast LLM inference (Llama 3.3 70B Versatile, Llama 3.1 8B Instant).
- **Pandas**: Data manipulation and DataFrame processing.
- **Pydantic**: Data schema validation and strict typing.
- **OpenPyXL**: Excel (`.xlsx`) spreadsheet parsing.

---

## 🚀 Quick Setup & Installation

### 1. Prerequisites
- Python 3.10 or higher installed.
- A free or paid [Groq API Key](https://console.groq.com/).

### 2. Clone Repository
```bash
git clone https://github.com/Shubham-coder-a/unihack-ai-product-intelligence.git
cd unihack-ai-product-intelligence
```

### 3. Create Virtual Environment
```bash
python -m venv .venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Environment & API Key Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

> [!IMPORTANT]
> Never commit your `.env` file or hardcode secrets into source code. `.env` is included in `.gitignore`.

---

## 💻 Usage Instructions

### Run the Application
```bash
streamlit run app/app.py
```

### Step-by-Step Dashboard Workflow
1. **Tab 1 (Upload Data)**: Drag-and-drop your product `.csv` or `.xlsx` file, OR click **📦 Load Sample Industrial Catalog** for an instant demo.
2. **Tab 2 (AI Pipeline)**: Select your desired Groq AI Model and batch processing size in the sidebar, then click **🚀 Run AI Enrichment Pipeline**.
3. **Tab 3 (Data Quality Audit)**: Review the data completeness uplift, resolved missing fields count, and overall quality grade (`A+` to `F`).
4. **Tab 4 (Product Explorer)**: Inspect individual records side-by-side (Raw Input JSON vs. AI Enriched Card & Spec Table).
5. **Tab 5 (Export Center)**: Click to download enriched data as CSV or JSON.

---

## 📊 Data Quality Audit Engine

The quality audit engine (`src/quality.py`) evaluates product records across completeness dimensions:
- **Field Completeness (%)**: Percentage of non-empty, non-null fields.
- **Completeness Uplift (%)**: $\text{Post-Enrichment Completeness} - \text{Pre-Enrichment Completeness}$.
- **Resolved Missing Fields**: Number of null/blank attributes filled by AI enrichment.
- **Technical Specs Extracted**: Count of key-value technical parameters normalized.
- **Quality Grading Scale**:
  - `A+` (90% – 100%)
  - `A` (80% – 89%)
  - `B` (70% – 79%)
  - `C` (50% – 69%)
  - `D` (30% – 49%)
  - `F` (< 30%)

---

## 🧪 Testing

Run the automated test suite using Python's built-in `unittest` runner:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

All 10 unit tests cover JSON cleaning, schema validation, prompt building, completeness scoring, audit grading, and sample data loading.

---

## 🌐 Streamlit Cloud Deployment Instructions

To deploy this application to **Streamlit Community Cloud**:
1. Push the repository to GitHub.
2. Log in to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Click **New App** and select repository `unihack-ai-product-intelligence`, branch `main`, and main file path `app/app.py`.
4. Under **Advanced Settings** -> **Secrets**, add your Groq API key:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key_here"
   ```
5. Click **Deploy!**

---

## 📄 License
MIT License. Developed for UniHack 2026.
