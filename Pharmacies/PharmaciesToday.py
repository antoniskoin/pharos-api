import requests
from bs4 import BeautifulSoup
from flask_restful import Resource


class PharmacyInformation(Resource):
    def get(self):
        pharmacy_information = {}

        req = requests.get("https://fsa-efimeries.gr/")
        soup = BeautifulSoup(req.content, "html.parser")
        table = soup.find("table", {"id": "table"})
        tbody = table.find("tbody")
        rows = tbody.find_all("tr")
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

            pharmacy_information[pharmacy] = {
                "area": area,
                "address": address,
                "phone": phone,
                "timetable": timetable,
                "status": status
            }

        return pharmacy_information
