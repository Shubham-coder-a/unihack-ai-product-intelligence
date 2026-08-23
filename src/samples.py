import os
import pandas as pd

# Resolve CSV path relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_CSV_PATH = os.path.join(BASE_DIR, "data", "sample_industrial_products.csv")


def load_sample_dataset() -> pd.DataFrame:
    """Load pre-built sample industrial product dataset."""
    if os.path.exists(SAMPLE_CSV_PATH):
        try:
            return pd.read_csv(SAMPLE_CSV_PATH)
        except Exception:
            pass
    
    # Fallback in-memory dataset if file reading fails
    data = [
        {
            "sku": "VALV-SS-100",
            "title": "1/2 NPT Ball Valve 316SS 1000PSI",
            "brand": "ValvTech",
            "category": "Valves",
            "raw_description": "Stainless steel ball valve 316 grade. Female NPT threads 1/2 in. Max pressure 1000 WOG. PTFE seat.",
            "price": 45.50,
            "in_stock": True
        },
        {
            "sku": "FAST-HEX-001",
            "title": "M8x1.25 Hex Head Cap Screw 304SS 30mm",
            "brand": "FastenPro",
            "category": "Fasteners",
            "raw_description": "M8 metric hex bolt, 30mm length, 1.25 pitch, 304 stainless steel DIN 933.",
            "price": 1.20,
            "in_stock": True
        },
        {
            "sku": "ELEC-CONT-40",
            "title": "24VDC 3-Pole 40A Industrial Contactor",
            "brand": "ElecControl",
            "category": None,
            "raw_description": "3P 40 amp power contactor with 24V DC coil voltage. DIN rail mounting.",
            "price": 78.00,
            "in_stock": False
        }
    ]
    return pd.DataFrame(data)
