import json
import re
from typing import Dict, Any
from groq import Groq
from src.config import GROQ_API_KEY, DEFAULT_MODEL
from src.schemas import EnrichedProduct


def clean_json_string(raw_text: str) -> str:
    """
    Extract and clean raw JSON string from LLM response.
    Strips markdown codeblocks (e.g. ```json ... ```) and leading/trailing whitespace.
    """
    if not raw_text:
        return "{}"
    
    text = raw_text.strip()
    
    # Strip markdown code blocks if present
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if match:
        text = match.group(1).strip()
    
    # Remove any leading prose before the first '{' and trailing prose after the last '}'
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        text = text[start_idx : end_idx + 1]
        
    return text


def build_enrichment_prompt(product_row: Dict[str, Any]) -> str:
    """Construct prompt for industrial product intelligence enrichment."""
    return f"""
You are an industrial commerce product data specialist.

Analyze this product record:

{json.dumps(product_row, default=str)}

Return ONLY valid JSON with these fields:

{{
  "product_title": "",
  "brand": "",
  "category": "",
  "product_type": "",
  "short_description": "",
  "key_features": [],
  "applications": [],
  "search_keywords": [],
  "technical_specs": {{}},
  "unspsc_category": "",
  "unspsc_code": ""
}}

Rules:
- "product_title": Standard, commerce-ready title (Brand + Model/Series + Product Type + Primary Specification).
- "brand": Brand or manufacturer name.
- "category": High-level product category.
- "product_type": Specific product classification.
- "short_description": Clear, technical commerce description.
- "key_features": List of main product features.
- "applications": Industrial applications/use cases.
- "search_keywords": Relevant B2B/industrial search & SEO tags.
- "technical_specs": Key-value dictionary of extracted technical attributes (e.g., "Material": "Stainless Steel 316", "Pressure Rating": "1000 PSI", "Thread Size": "1/2 inch NPT").
- "unspsc_category": Standard UNSPSC taxonomy commodity name.
- "unspsc_code": Standard 8-digit UNSPSC code (if known, else empty string).
- Do not invent non-existent technical specs; derive only from input.
- If information is missing, use an empty string, empty list, or empty object.
"""


class GroqProductEnricher:
    """Client wrapper for Groq AI product enrichment."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or GROQ_API_KEY
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is missing. Please set it in your environment or .env file.")
        self.client = Groq(api_key=self.api_key)

    def enrich_product(self, row: Dict[str, Any], model_name: str = DEFAULT_MODEL) -> Dict[str, Any]:
        """
        Enrich a single product record using Groq LLM.
        Returns standard dictionary with enriched fields.
        """
        prompt = build_enrichment_prompt(row)
        
        try:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            raw_text = response.choices[0].message.content
            cleaned_json = clean_json_string(raw_text)
            
            try:
                data = json.loads(cleaned_json)
                
                # Ensure technical_specs is a dictionary
                if "technical_specs" in data and not isinstance(data["technical_specs"], dict):
                    if isinstance(data["technical_specs"], list):
                        # Convert list of dicts to dict if model returned list format
                        specs_dict = {}
                        for item in data["technical_specs"]:
                            if isinstance(item, dict) and "name" in item and "value" in item:
                                specs_dict[item["name"]] = str(item["value"])
                            elif isinstance(item, dict):
                                specs_dict.update({str(k): str(v) for k, v in item.items()})
                        data["technical_specs"] = specs_dict
                    else:
                        data["technical_specs"] = {}

                enriched = EnrichedProduct(**data).to_dict()
            except Exception:
                # Fallback if structure parsing fails slightly
                enriched = EnrichedProduct(
                    short_description=raw_text
                ).to_dict()
                
            return enriched

        except Exception as e:
            # Fallback error record
            return EnrichedProduct(
                short_description=f"AI Error: {str(e)}"
            ).to_dict()
