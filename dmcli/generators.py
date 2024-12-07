from os import getenv

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from result import Err, Ok, Result  # type: ignore

load_dotenv()


class Generator:
    def __init__(self):
        self.url_base = "https://chartopia.d12dev.com/api/charts/"

    def generate(self, chart_id: str) -> Result:
        try:
            assert (
                getenv("CHARTOPIA_USER") is not None
                and getenv("CHARTOPIA_PASS") is not None
            )
        except AssertionError:
            return Err(
                "Please set your CHARTOPIA_USER and CHARTOPIA_PASS environment variables"
            )
        auth = HTTPBasicAuth(
            getenv("CHARTOPIA_USER"), getenv("CHARTOPIA_PASS")
        )
        url = f"{self.url_base}{chart_id}/roll/"
        response = requests.post(url, data={"mult": "1"}, auth=auth)
        return Ok(response.json())


class TavernGenerator(Generator):
    def __init__(self):
        super().__init__()
        self.chart_id = "114"

    def generate(self):
        return super().generate(self.chart_id)
