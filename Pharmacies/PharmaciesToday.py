import requests
from bs4 import BeautifulSoup
from flask_restful import Resource
from helpers.common import get_headers


class PharmacyInformation(Resource):
    def get(self):
        pharmacy_information = {}

        req = requests.get("https://fsa-efimeries.gr/", headers=get_headers())

        if req.status_code != 200:
            return f"Request failed with status code {req.status_code}"

        soup = BeautifulSoup(req.content, "html.parser")
        table = soup.find("table", {"id": "table"})
        tbody = table.find("tbody")
        rows = tbody.find_all("tr")
        pharmacy_count = 0
        for row in rows:
            try:
                columns = row.find_all("td")
                area = columns[2].text.strip()
                pharmacy = columns[3].text.strip()
                address = columns[4].text.strip()
                phone = columns[5].text.strip()
                timetable = columns[6].text.strip()
                status = columns[7].text.strip()
            except Exception as error:
                return f"An error occurred: {error}"

            if status:
                status = "OPEN"
            else:
                status = "CLOSED"

            pharmacy_information[pharmacy_count] = {
                "pharmacy": pharmacy,
                "area": area,
                "address": address,
                "phone": phone,
                "timetable": timetable,
                "status": status
            }

            pharmacy_count += 1

        return pharmacy_information
