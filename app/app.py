import os
import json
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.set_page_config(
    page_title="AI Product Intelligence",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Product Intelligence")
st.subheader("Industrial Commerce Product Data Enrichment")
st.write(
    "Upload industrial product data and generate structured, "
    "commerce-ready product information using AI."
)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

uploaded_file = st.file_uploader(
    "Upload Product Dataset",
    type=["csv", "xlsx"]
)

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Dataset uploaded successfully!")

    st.subheader("Input Data")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("AI Product Enrichment")

    if st.button("🚀 Generate AI Enrichment"):

        progress = st.progress(0)
        results = []

        total = min(len(df), 10)

        for i in range(total):

            row = df.iloc[i].to_dict()

            prompt = f"""
You are an industrial commerce product data specialist.

Analyze this product record:

{json.dumps(row, default=str)}

Return ONLY valid JSON with these fields:

{{
  "product_title": "",
  "brand": "",
  "category": "",
  "product_type": "",
  "short_description": "",
  "key_features": [],
  "applications": [],
  "search_keywords": []
}}

Rules:
- Do not invent technical specifications.
- Use only information available in the input.
- If information is missing, use an empty string or empty list.
- Make the output suitable for industrial e-commerce.
"""

            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.1
                )

                text = response.choices[0].message.content

                try:
                    enriched = json.loads(text)
                except:
                    enriched = {
                        "product_title": "",
                        "brand": "",
                        "category": "",
                        "product_type": "",
                        "short_description": text,
                        "key_features": [],
                        "applications": [],
                        "search_keywords": []
                    }

                results.append(enriched)

            except Exception as e:
                results.append({
                    "product_title": "",
                    "brand": "",
                    "category": "",
                    "product_type": "",
                    "short_description": f"AI Error: {str(e)}",
                    "key_features": [],
                    "applications": [],
                    "search_keywords": []
                })

            progress.progress((i + 1) / total)

        enriched_df = pd.DataFrame(results)

        st.subheader("✨ AI Generated Product Intelligence")
        st.dataframe(enriched_df, use_container_width=True)

        csv = enriched_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Enriched CSV",
            csv,
            "ai_enriched_products.csv",
            "text/csv"
        )

        st.success("AI enrichment completed!")