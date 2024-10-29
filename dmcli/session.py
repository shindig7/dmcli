import json
from pathlib import Path
from uuid import uuid4 as uuid

from dmcli.character import NPC, PC


class Session:
    def __init__(self, name: str):
        self.name = name
        self._id = uuid()
        self.pcs = []
        self.npcs = []
        self.monsters = []

    def load_character(self, file_path: Path) -> None:
        assert file_path.suffix == ".json", "File must be a JSON file"
        with open(file_path, "r") as f:
            data = json.load(f)

        match data["type"]:
            case "NPC":
                self.npcs.append(NPC.create_from_json(data))
            case "PC":
                self.pcs.append(PC.create_from_json(data))
