import datetime
from requests import Session
from bs4 import BeautifulSoup
from flask_restful import Resource


class SpecificPharmaciesToday(Resource):
    def get(self):
        specific_area_info = {}
        session = Session()
        user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
        req = session.get("https://fsa-efimeries.gr/", headers={"user-agent": user_agent})
        verification_cookie = req.cookies.get(".AspNetCore.Antiforgery._7w_lBqvcBI")
        date_today = datetime.datetime.now()
        formatted_date = date_today.strftime("%Y-%m-%d")
        data = {
            "Date": formatted_date,
            "PerioxiId": 1,
            "isOpen": "false",
            "__RequestVerificationToken": verification_cookie,
            "IsOpen": "false"
        }
        req = session.post("https://fsa-efimeries.gr/", data=data, headers={"user-agent": user_agent})
        soup = BeautifulSoup(req.content, "html.parser")
        table = soup.find("table", {"id": "table"})
        tbody = table.find("tbody")
        rows = tbody.find_all("tr")
        for row in rows:
            try:
                columns = row.find_all("td")
                print(columns)
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

            specific_area_info[pharmacy] = {
                "area": area,
                "address": address,
                "phone": phone,
                "timetable": timetable,
                "status": status
            }

        return specific_area_info
