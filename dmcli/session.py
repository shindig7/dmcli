import json
from pathlib import Path
from uuid import uuid4 as uuid

from result import Err, Ok

from dmcli.character import NPC, PC, Monster


class Session:
    def __init__(self):
        self.name = None
        self._id = uuid()
        self.pcs = {}
        self.npcs = {}
        self.monsters = {}

    def name_session(self, name: str) -> None:
        self.name = name

    def load_character(self, file_path: Path) -> None:
        assert file_path.suffix == ".json", "File must be a JSON file"
        with open(file_path, "r") as f:
            data = json.load(f)

        match data["type"]:
            case "NPC":
                character = NPC.create_from_json(data)
                self.npcs[character.nickname] = character
            case "PC":
                character = PC.create_from_json(data)
                self.pcs[character.nickname] = character
            case "Monster":
                character = Monster.create_from_json(data)
                self.monsters[character.nickname] = character
            case _:
                raise ValueError(f"Invalid character type: {data['type']}")

    def save_session(self) -> None:
        if self.name is None:
            return Err(ValueError("Session must have a name"))
        data = {
            "name": self.name,
            "id": str(self._id),
            "pcs": {nickname: pc.dict() for nickname, pc in self.pcs},
            "npcs": {nickname: npc.dict() for nickname, npc in self.npcs},
        }
        file_path = Path(f"{self.name}.json")
        with open(file_path, "w") as f:
            json.dump(data, f)

        return Ok(f"Session saved to {file_path}")

    def load_party(self, folder_path: Path) -> None:
        for file_path in folder_path.rglob("*.json"):
            with open(file_path, "r") as f:
                character = json.load(f)
            match character["type"]:
                case "NPC":
                    character = NPC.create_from_json(character)
                    self.npcs[character.nickname] = character
                case "PC":
                    character = PC.create_from_json(character)
                    self.pcs[character.nickname] = character
                case "Monster":
                    character = Monster.create_from_json(character)
                    self.monsters[character.nickname] = character
                case _:
                    return Err(
                        ValueError(
                            f"Invalid character type: {character['type']}"
                        )
                    )
        return Ok("Party loaded")

    def __str__(self):
        return f"Session: {self.name}"
