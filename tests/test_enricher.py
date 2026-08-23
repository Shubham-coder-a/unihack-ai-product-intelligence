import unittest
import json
from src.enricher import clean_json_string, build_enrichment_prompt
from src.schemas import EnrichedProduct


class TestEnricher(unittest.TestCase):

    def test_clean_json_string_with_markdown(self):
        raw_response = """
        Here is the response:
        ```json
        {
          "product_title": "Heavy Duty Industrial Ball Valve",
          "brand": "ValvTech",
          "category": "Valves",
          "product_type": "Ball Valve",
          "short_description": "High pressure stainless ball valve",
          "key_features": ["316 Stainless", "Full Port"],
          "applications": ["Oil & Gas"],
          "search_keywords": ["valve", "stainless"]
        }
        ```
        Hope this helps!
        """
        cleaned = clean_json_string(raw_response)
        data = json.loads(cleaned)
        self.assertEqual(data["product_title"], "Heavy Duty Industrial Ball Valve")
        self.assertEqual(data["brand"], "ValvTech")
        self.assertIn("316 Stainless", data["key_features"])

    def test_clean_json_string_plain(self):
        raw_response = '{"product_title": "Test Title", "brand": "BrandX"}'
        cleaned = clean_json_string(raw_response)
        data = json.loads(cleaned)
        self.assertEqual(data["product_title"], "Test Title")

    def test_schema_defaults(self):
        product = EnrichedProduct(product_title="Sample Valve")
        product_dict = product.to_dict()
        self.assertEqual(product_dict["product_title"], "Sample Valve")
        self.assertIsInstance(product_dict["key_features"], list)
        self.assertEqual(product_dict["brand"], "")

    def test_build_enrichment_prompt(self):
        row = {"sku": "VALVE-123", "name": "1-Inch Stainless Valve"}
        prompt = build_enrichment_prompt(row)
        self.assertIn("VALVE-123", prompt)
        self.assertIn("1-Inch Stainless Valve", prompt)


if __name__ == "__main__":
    unittest.main()
