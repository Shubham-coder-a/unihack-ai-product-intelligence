from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TechnicalSpec(BaseModel):
    """Key-value pair for normalized technical specification."""
    name: str
    value: str


class EnrichedProduct(BaseModel):
    """Schema representing an AI-enriched industrial commerce product record."""
    product_title: str = Field(default="", description="Clean, standard industrial product title")
    brand: str = Field(default="", description="Manufacturer or brand name")
    category: str = Field(default="", description="High-level product category")
    product_type: str = Field(default="", description="Specific product type or subtype")
    short_description: str = Field(default="", description="Commerce-ready product description")
    key_features: List[str] = Field(default_factory=list, description="Bullet points of key product features")
    applications: List[str] = Field(default_factory=list, description="Industrial applications or use cases")
    search_keywords: List[str] = Field(default_factory=list, description="Relevant search & SEO keywords")
    technical_specs: Dict[str, str] = Field(default_factory=dict, description="Normalized technical specification key-value pairs")
    unspsc_category: str = Field(default="", description="UNSPSC taxonomy standard category name")
    unspsc_code: str = Field(default="", description="UNSPSC 8-digit commodity code")

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to standard dictionary format."""
        return {
            "product_title": self.product_title,
            "brand": self.brand,
            "category": self.category,
            "product_type": self.product_type,
            "short_description": self.short_description,
            "key_features": self.key_features,
            "applications": self.applications,
            "search_keywords": self.search_keywords,
            "technical_specs": self.technical_specs,
            "unspsc_category": self.unspsc_category,
            "unspsc_code": self.unspsc_code,
        }


class DataQualityAudit(BaseModel):
    """Data quality and completeness audit metrics for a dataset or row."""
    pre_completeness_pct: float = 0.0
    post_completeness_pct: float = 0.0
    completeness_uplift_pct: float = 0.0
    total_fields_evaluated: int = 0
    resolved_missing_fields: int = 0
    specs_extracted_count: int = 0
    quality_grade: str = "C"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pre_completeness_pct": round(self.pre_completeness_pct, 1),
            "post_completeness_pct": round(self.post_completeness_pct, 1),
            "completeness_uplift_pct": round(self.completeness_uplift_pct, 1),
            "total_fields_evaluated": self.total_fields_evaluated,
            "resolved_missing_fields": self.resolved_missing_fields,
            "specs_extracted_count": self.specs_extracted_count,
            "quality_grade": self.quality_grade,
        }
