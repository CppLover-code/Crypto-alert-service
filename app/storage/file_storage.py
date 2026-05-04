import json
from pathlib import Path
from typing import Dict, Any, List

class FileStorage:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

        # создаем файл, если его нет
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.__write([])

    def save(self)