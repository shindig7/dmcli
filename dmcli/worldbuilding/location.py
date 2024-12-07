from pydantic import BaseModel


class Settlement(BaseModel):
    name: str
    description: str
    population: int
    region: str | None

    @property
    def classification(self):
        if self.population < 100:
            return "village"
        elif self.population < 6000:
            return "town"
        elif self.population < 20_000:
            return "city"
        else:
            return "metropolis"
