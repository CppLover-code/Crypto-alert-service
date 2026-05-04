import json
from pathlib import Path
from typing import Dict, Any, List

class FileStorage:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

        # создаем файл, если его нет
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self._write([])

    def save(self, data: Dict[str, Any]) -> None:
        # добавляет новую запись в файл

        current_data = self._read()
        current_data.append(data)
        self._write(current_data)

    def _read(self) -> List[Dict[str, Any]]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
        
    def _write(self, data: List[Dict[str,Any]]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)