import json
from pathlib import Path
from uuid import uuid4 as uuid

from dmcli.character import NPC, PC


class Session:
    def __init__(self):
        self.name = None
        self._id = uuid()
        self.pcs = []
        self.npcs = []
        self.monsters = []

    def name_session(self, name: str) -> None:
        self.name = name

    def load_character(self, file_path: Path) -> None:
        assert file_path.suffix == ".json", "File must be a JSON file"
        with open(file_path, "r") as f:
            data = json.load(f)

        match data["type"]:
            case "NPC":
                self.npcs.append(NPC.create_from_json(data))
            case "PC":
                self.pcs.append(PC.create_from_json(data))
            case _:
                raise ValueError(f"Invalid character type: {data['type']}")

    def save_session(self) -> None:
        if self.name is None:
            raise ValueError("Session must have a name")
        data = {
            "name": self.name,
            "id": str(self._id),
            "pcs": [pc.to_dict() for pc in self.pcs],
            "npcs": [npc.to_dict() for npc in self.npcs],
            "monsters": [monster.to_dict() for monster in self.monsters],
        }
        file_path = Path(f"{self.name}.json")
        with open(file_path, "w") as f:
            json.dump(data, f)
