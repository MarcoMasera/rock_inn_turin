from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Optional

from app.models import PropertyBaseInfo


class PropertyRepository:
    def __init__(self, db_path: str = "app/data/properties.json") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self._save({})

    def _load(self) -> Dict[str, dict]:
        return json.loads(self.db_path.read_text(encoding="utf-8"))

    def _save(self, payload: Dict[str, dict]) -> None:
        self.db_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def upsert(self, property_info: PropertyBaseInfo) -> PropertyBaseInfo:
        data = self._load()
        data[property_info.property_id] = property_info.model_dump()
        self._save(data)
        return property_info

    def get(self, property_id: str) -> Optional[PropertyBaseInfo]:
        data = self._load()
        payload = data.get(property_id)
        if not payload:
            return None
        return PropertyBaseInfo(**payload)
