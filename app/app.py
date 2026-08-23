import os
import json
import pandas as pd
import streamlit as st
from src.config import GROQ_API_KEY, AVAILABLE_MODELS, DEFAULT_MODEL
from src.enricher import GroqProductEnricher
from src.quality import audit_dataset, audit_product_record
from src.samples import load_sample_dataset

# Streamlit Page Configuration
st.set_page_config(
    page_title="AI Product Intelligence Dashboard | UniHack 2026",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling for Premium Aesthetics
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .badge-pill {
        background-color: #EFF6FF;
        color: #1D4ED8;
        padding: 0.35rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-right: 0.5rem;
        border: 1px solid #BFDBFE;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
    }
    .stProgress > div > div > div > div {
        background-color: #2563EB;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar Title & Badges
st.markdown('<div class="main-header">⚡ AI Product Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Industrial Commerce Data Enrichment & Quality Audit Engine</div>', unsafe_allow_html=True)
st.markdown("""
<div>
    <span class="badge-pill">🏆 UniHack 2026</span>
    <span class="badge-pill">🚀 Groq Llama-3.3 Powered</span>
    <span class="badge-pill">🏭 B2B Commerce Ready</span>
    <span class="badge-pill">📊 UNSPSC / ETIM Enabled</span>
</div>
<br>
""", unsafe_allow_html=True)

# Sidebar Configuration Controls
st.sidebar.title("⚙️ Dashboard Controls")

selected_model_label = st.sidebar.selectbox(
    "AI Engine Model",
    options=list(AVAILABLE_MODELS.keys()),
    index=0,
    help="Select the Groq LLM architecture for product data enrichment."
)
selected_model = AVAILABLE_MODELS[selected_model_label]

api_key = GROQ_API_KEY or os.getenv("GROQ_API_KEY")

if api_key:
    st.sidebar.success("🔑 API Key Loaded")
else:
    st.sidebar.error("❌ GROQ_API_KEY Missing")
    st.error("GROQ_API_KEY not found. Please verify your .env configuration.")
    st.stop()

# Initialize Enricher client
try:
    enricher = GroqProductEnricher(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize Groq AI Enricher: {str(e)}")
    st.stop()

# Initialize Session State Variables
if "dataset" not in st.session_state:
    st.session_state["dataset"] = None
if "enriched_df" not in st.session_state:
    st.session_state["enriched_df"] = None
if "audit_report" not in st.session_state:
    st.session_state["audit_report"] = None

# Main Tabs Navigation
tab_upload, tab_process, tab_quality, tab_explorer, tab_export = st.tabs([
    "📥 1. Upload Data",
    "🚀 2. AI Pipeline",
    "📊 3. Data Quality Audit",
    "🔍 4. Product Explorer",
    "⬇️ 5. Export Center"
])

# ---------------------------------------------------------
# TAB 1: UPLOAD DATA & SOURCE SELECTION
# ---------------------------------------------------------
with tab_upload:
    st.subheader("Data Source Selection")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload Industrial Product File (.csv or .xlsx)",
            type=["csv", "xlsx"],
            help="Upload raw catalog datasets containing SKU, title, brand, description, specs, etc."
        )
        if uploaded_file:
            if uploaded_file.name.endswith(".csv"):
                st.session_state["dataset"] = pd.read_csv(uploaded_file)
            else:
                st.session_state["dataset"] = pd.read_excel(uploaded_file)
            st.session_state["enriched_df"] = None
            st.session_state["audit_report"] = None
            st.success(f"File uploaded successfully: {uploaded_file.name}")
            
    with col2:
        st.write("#### Quick Demo Test")
        st.write("No catalog file available? Load our pre-configured industrial sample dataset:")
        if st.button("📦 Load Sample Industrial Catalog", use_container_width=True):
            st.session_state["dataset"] = load_sample_dataset()
            st.session_state["enriched_df"] = None
            st.session_state["audit_report"] = None
            st.success("Loaded sample industrial product dataset!")

    if st.session_state["dataset"] is not None:
        df = st.session_state["dataset"]
        st.markdown("---")
        st.subheader("Input Dataset Overview")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Total Records", len(df))
        m_col2.metric("Total Columns", len(df.columns))
        m_col3.metric("Detected Format", "Pandas DataFrame")
        
        st.dataframe(df.head(20), use_container_width=True)

# ---------------------------------------------------------
# TAB 2: AI ENRICHMENT PIPELINE
# ---------------------------------------------------------
with tab_process:
    st.subheader("AI Batch Enrichment Pipeline")
    
    if st.session_state["dataset"] is None:
        st.warning("⚠️ Please upload a dataset or load the sample catalog in Tab 1 first.")
    else:
        df = st.session_state["dataset"]
        
        max_rows = len(df)
        default_batch = min(max_rows, 10)
        
        batch_size = st.sidebar.slider(
            "Batch Processing Limit",
            min_value=1,
            max_value=max_rows,
            value=default_batch,
            help="Select maximum number of records to enrich in this run."
        )
        
        st.info(f"Target Batch: **{batch_size}** of {max_rows} records using **{selected_model_label}**.")
        
        if st.button("🚀 Run AI Enrichment Pipeline", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            
            for i in range(batch_size):
                row = df.iloc[i].to_dict()
                status_text.text(f"Enriching record {i+1} of {batch_size}...")
                
                enriched = enricher.enrich_product(row, model_name=selected_model)
                results.append(enriched)
                
                progress_bar.progress((i + 1) / batch_size)
            
            status_text.text("AI Enrichment Completed Successfully!")
            st.session_state["enriched_df"] = pd.DataFrame(results)
            st.session_state["audit_report"] = audit_dataset(df.iloc[:batch_size], st.session_state["enriched_df"])
            st.success("Enrichment process finished! Explore results in Tabs 3, 4, and 5.")

        if st.session_state["enriched_df"] is not None:
            st.markdown("---")
            st.subheader("✨ AI Enriched Output Data")
            st.dataframe(st.session_state["enriched_df"], use_container_width=True)

# ---------------------------------------------------------
# TAB 3: DATA QUALITY AUDIT DASHBOARD
# ---------------------------------------------------------
with tab_quality:
    st.subheader("📊 Data Quality & Completeness Audit")
    
    if st.session_state["audit_report"] is None:
        st.info("Run the AI Enrichment Pipeline in Tab 2 to generate data quality audit metrics.")
    else:
        audit = st.session_state["audit_report"]
        
        q1, q2, q3, q4 = st.columns(4)
        q1.metric("Pre-Enrichment Completeness", f"{audit['pre_completeness_pct']}%")
        q2.metric("Post-Enrichment Completeness", f"{audit['post_completeness_pct']}%", delta=f"+{audit['completeness_uplift_pct']}%")
        q3.metric("Resolved Missing Fields", audit['total_resolved_missing_fields'])
        q4.metric("Quality Grade", audit['overall_quality_grade'])
        
        st.markdown("---")
        st.subheader("Audit Insights Summary")
        
        st.write(f"- **Total Products Evaluated**: {audit['total_records_processed']}")
        st.write(f"- **Technical Specs Extracted**: {audit['total_specs_extracted']} key-value attributes")
        st.write(f"- **Completeness Uplift**: Improved data completeness by **+{audit['completeness_uplift_pct']}%**")
        st.write(f"- **Quality Grade**: **{audit['overall_quality_grade']}**")

# ---------------------------------------------------------
# TAB 4: INTERACTIVE PRODUCT EXPLORER
# ---------------------------------------------------------
with tab_explorer:
    st.subheader("🔍 Side-by-Side Product Explorer")
    
    if st.session_state["enriched_df"] is None or st.session_state["dataset"] is None:
        st.info("Run AI Enrichment in Tab 2 to enable product inspection.")
    else:
        raw_df = st.session_state["dataset"]
        enriched_df = st.session_state["enriched_df"]
        
        num_items = len(enriched_df)
        item_idx = st.selectbox(
            "Select Product to Inspect:",
            options=list(range(num_items)),
            format_func=lambda i: f"Row {i+1}: {enriched_df.iloc[i].get('product_title') or raw_df.iloc[i].get('title') or f'Item #{i+1}'}"
        )
        
        raw_item = raw_df.iloc[item_idx].to_dict()
        enriched_item = enriched_df.iloc[item_idx].to_dict()
        
        col_raw, col_enriched = st.columns(2)
        
        with col_raw:
            st.markdown("### 📄 Raw Input Data")
            st.json(raw_item)
            
        with col_enriched:
            st.markdown("### ✨ AI Enriched Card")
            st.markdown(f"**Title**: {enriched_item.get('product_title')}")
            st.markdown(f"**Brand**: `{enriched_item.get('brand')}` | **Category**: `{enriched_item.get('category')}`")
            st.markdown(f"**UNSPSC Code**: `{enriched_item.get('unspsc_code')}` ({enriched_item.get('unspsc_category')})")
            st.markdown(f"**Description**: {enriched_item.get('short_description')}")
            
            st.markdown("**Key Features:**")
            features = enriched_item.get('key_features', [])
            if isinstance(features, list) and len(features) > 0:
                for f in features:
                    st.write(f"- {f}")
            else:
                st.write("*None listed*")
                
            st.markdown("**Technical Specs:**")
            specs = enriched_item.get('technical_specs', {})
            if isinstance(specs, dict) and len(specs) > 0:
                spec_df = pd.DataFrame(list(specs.items()), columns=["Specification", "Value"])
                st.table(spec_df)
            else:
                st.write("*No technical specifications extracted*")

# ---------------------------------------------------------
# TAB 5: EXPORT CENTER
# ---------------------------------------------------------
with tab_export:
    st.subheader("⬇️ Export Enriched Product Intelligence")
    
    if st.session_state["enriched_df"] is None:
        st.info("Run AI Enrichment in Tab 2 to generate exportable files.")
    else:
        enriched_df = st.session_state["enriched_df"]
        
        csv_data = enriched_df.to_csv(index=False).encode("utf-8")
        json_data = enriched_df.to_json(orient="records", indent=2).encode("utf-8")
        
        e_col1, e_col2 = st.columns(2)
        
        with e_col1:
            st.write("#### 📄 CSV Format")
            st.write("Ideal for Excel, databases, and e-commerce bulk imports.")
            st.download_button(
                "⬇️ Download Enriched CSV",
                csv_data,
                "ai_enriched_products.csv",
                "text/csv",
                use_container_width=True
            )
            
        with e_col2:
            st.write("#### 🌐 JSON Format")
            st.write("Ideal for REST API integrations, PIM systems, and search indexes.")
            st.download_button(
                "⬇️ Download Enriched JSON",
                json_data,
                "ai_enriched_products.json",
                "application/json",
                use_container_width=True
            )
            
        st.success("Enriched data is ready for enterprise integration!")