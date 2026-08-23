import unittest
import pandas as pd
from src.quality import (
    is_value_present,
    calculate_row_completeness,
    calculate_quality_grade,
    audit_product_record,
    audit_dataset
)
from src.samples import load_sample_dataset


class TestDataQualityAudit(unittest.TestCase):

    def test_is_value_present(self):
        self.assertTrue(is_value_present("Valid Text"))
        self.assertTrue(is_value_present(["feature1"]))
        self.assertTrue(is_value_present({"spec1": "val1"}))
        self.assertFalse(is_value_present(""))
        self.assertFalse(is_value_present("   "))
        self.assertFalse(is_value_present(None))
        self.assertFalse(is_value_present("N/A"))
        self.assertFalse(is_value_present([]))
        self.assertFalse(is_value_present({}))

    def test_calculate_row_completeness(self):
        row_full = {"a": "val1", "b": "val2", "c": "val3"}
        self.assertEqual(calculate_row_completeness(row_full), 100.0)

        row_partial = {"a": "val1", "b": "", "c": None, "d": "val4"}
        self.assertEqual(calculate_row_completeness(row_partial), 50.0)

    def test_calculate_quality_grade(self):
        self.assertEqual(calculate_quality_grade(95.0), "A+")
        self.assertEqual(calculate_quality_grade(85.0), "A")
        self.assertEqual(calculate_quality_grade(75.0), "B")
        self.assertEqual(calculate_quality_grade(60.0), "C")
        self.assertEqual(calculate_quality_grade(40.0), "D")
        self.assertEqual(calculate_quality_grade(20.0), "F")

    def test_audit_product_record(self):
        raw_row = {
            "title": "Ball Valve",
            "brand": "",
            "category": None,
            "description": ""
        }
        enriched_row = {
            "product_title": "1/2 Industrial Ball Valve",
            "brand": "ValvTech",
            "category": "Valves",
            "short_description": "High pressure valve",
            "technical_specs": {"Material": "Stainless Steel"}
        }

        audit = audit_product_record(raw_row, enriched_row)
        self.assertGreater(audit.post_completeness_pct, audit.pre_completeness_pct)
        self.assertGreater(audit.completeness_uplift_pct, 0)
        self.assertEqual(audit.specs_extracted_count, 1)

    def test_audit_dataset(self):
        raw_df = pd.DataFrame([
            {"sku": "1", "title": "Valve", "category": ""},
            {"sku": "2", "title": "Bolt", "category": None}
        ])
        enriched_df = pd.DataFrame([
            {"product_title": "Valve", "category": "Valves", "technical_specs": {"Mat": "SS"}},
            {"product_title": "Bolt", "category": "Fasteners", "technical_specs": {"Pitch": "1.25"}}
        ])

        report = audit_dataset(raw_df, enriched_df)
        self.assertIn("pre_completeness_pct", report)
        self.assertIn("post_completeness_pct", report)
        self.assertIn("completeness_uplift_pct", report)
        self.assertEqual(report["total_records_processed"], 2)

    def test_load_sample_dataset(self):
        df = load_sample_dataset()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("sku", df.columns)


if __name__ == "__main__":
    unittest.main()
