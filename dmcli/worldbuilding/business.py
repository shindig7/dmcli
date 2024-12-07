from pydantic import BaseModel, field_validator

from dmcli.character import NPC


class Business(BaseModel):
    name: str
    description: str
    owner: str
    location: str

    @classmethod
    def create_from_json(cls, data):
        return cls(**data)

    def __str__(self):
        return f"{self.name} is a business owned by {self.owner} in {self.location}"

    def __repr__(self):
        return self.__str__()


class ClassinessMixin(BaseModel):
    classiness: int | None

    @field_validator("classiness")
    def classiness_validator(cls, v):
        if v is not None:
            assert v in range(1, 6), "Classiness must be between 1 and 5"
        return v


class FoodAndDrinkMixin(BaseModel):
    food: list[str] | None
    drinks: list[str] | None


class Tavern(Business, FoodAndDrinkMixin):
    patrons: list[str] | NPC | None


class Inn(Business, FoodAndDrinkMixin):
    rooms: int
    star_level: int | None
