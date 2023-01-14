import requests
from bs4 import BeautifulSoup
from flask_restful import Resource


class Locations(Resource):
    def get(self):
        url = "https://www.xo.gr/efimerevonta-nosokomeia/"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            popular_hospitals = soup.find("div", {"id": "HospitalArea"})
            rows = popular_hospitals.find_all("li")

            areas = {}
            i = 0
            for row in rows:
                area = row.find("a")
                area = area["href"]
                area = area.split("/")
                area = area[2]
                area[i] = area

            return areas
        else:
            return None
