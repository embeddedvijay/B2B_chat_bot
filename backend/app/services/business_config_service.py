import json
from pathlib import Path

class BusinessConfigService:
    def __init__(self):
        self.path = Path(__file__).resolve().parents[3] / "config" / "businesses.json"

    def get(self, business_id: str) -> dict:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return data.get(business_id, data["default"])
