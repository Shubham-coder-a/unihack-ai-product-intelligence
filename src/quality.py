import pandas as pd
import numpy as np
from typing import Dict, Any, List
from src.schemas import DataQualityAudit


def is_value_present(val: Any) -> bool:
    """Check if a field value is non-empty and non-null."""
    if val is None:
        return False
    if isinstance(val, (float, int)) and (np.isnan(val) if isinstance(val, float) else False):
        return False
    if isinstance(val, str):
        cleaned = val.strip().lower()
        if not cleaned or cleaned in ["none", "null", "nan", "n/a", "unknown", ""]:
            return False
        return True
    if isinstance(val, (list, dict)):
        return len(val) > 0
    return bool(val)


def calculate_row_completeness(row: Dict[str, Any]) -> float:
    """Calculate completeness percentage (0-100) for a single record."""
    if not row:
        return 0.0
    
    total_fields = len(row)
    if total_fields == 0:
        return 0.0
    
    present_fields = sum(1 for v in row.values() if is_value_present(v))
    return (present_fields / total_fields) * 100.0


def calculate_quality_grade(score_pct: float) -> str:
    """Assign letter grade based on completeness score percentage."""
    if score_pct >= 90.0:
        return "A+"
    elif score_pct >= 80.0:
        return "A"
    elif score_pct >= 70.0:
        return "B"
    elif score_pct >= 50.0:
        return "C"
    elif score_pct >= 30.0:
        return "D"
    else:
        return "F"


def audit_product_record(raw_row: Dict[str, Any], enriched_row: Dict[str, Any]) -> DataQualityAudit:
    """
    Perform audit comparison between raw input record and AI-enriched output record.
    """
    pre_score = calculate_row_completeness(raw_row)
    post_score = calculate_row_completeness(enriched_row)
    
    uplift = max(0.0, post_score - pre_score)
    
    raw_missing_count = sum(1 for v in raw_row.values() if not is_value_present(v))
    enriched_missing_count = sum(1 for v in enriched_row.values() if not is_value_present(v))
    resolved_count = max(0, raw_missing_count - enriched_missing_count)
    
    # Specs extracted count
    specs = enriched_row.get("technical_specs", {})
    specs_count = len(specs) if isinstance(specs, dict) else (len(specs) if isinstance(specs, list) else 0)
    
    grade = calculate_quality_grade(post_score)
    
    return DataQualityAudit(
        pre_completeness_pct=pre_score,
        post_completeness_pct=post_score,
        completeness_uplift_pct=uplift,
        total_fields_evaluated=len(enriched_row),
        resolved_missing_fields=resolved_count,
        specs_extracted_count=specs_count,
        quality_grade=grade
    )


def audit_dataset(raw_df: pd.DataFrame, enriched_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate dataset-wide quality metrics comparing raw input dataset with enriched output dataset.
    """
    if raw_df.empty or enriched_df.empty:
        return DataQualityAudit().to_dict()
    
    num_rows = min(len(raw_df), len(enriched_df))
    
    total_pre_score = 0.0
    total_post_score = 0.0
    total_resolved = 0
    total_specs = 0
    
    for i in range(num_rows):
        raw_row = raw_df.iloc[i].to_dict()
        enriched_row = enriched_df.iloc[i].to_dict()
        
        audit_res = audit_product_record(raw_row, enriched_row)
        total_pre_score += audit_res.pre_completeness_pct
        total_post_score += audit_res.post_completeness_pct
        total_resolved += audit_res.resolved_missing_fields
        total_specs += audit_res.specs_extracted_count
    
    avg_pre = total_pre_score / num_rows if num_rows > 0 else 0.0
    avg_post = total_post_score / num_rows if num_rows > 0 else 0.0
    avg_uplift = max(0.0, avg_post - avg_pre)
    overall_grade = calculate_quality_grade(avg_post)
    
    return {
        "pre_completeness_pct": round(avg_pre, 1),
        "post_completeness_pct": round(avg_post, 1),
        "completeness_uplift_pct": round(avg_uplift, 1),
        "total_records_processed": num_rows,
        "total_resolved_missing_fields": total_resolved,
        "total_specs_extracted": total_specs,
        "overall_quality_grade": overall_grade
    }
