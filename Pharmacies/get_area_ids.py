from bs4 import BeautifulSoup
from flask_restful import Resource
import requests


class AreaID(Resource):
    def get(self):
        area_ids = {}
        url = "https://fsa-efimeries.gr"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            dropdown = soup.find("select", {"id": "PerioxiId"})
            areas = dropdown.find_all("option")

            for area in areas:
                area_name = area.text.strip()
                area_id = area["value"]
                area_ids[area_name] = area_id

            return area_ids
        else:
            return None
