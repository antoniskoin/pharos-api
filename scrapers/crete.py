import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_crete_pharmacies_today() -> dict:
    today = datetime.today()
    formatted_date = today.strftime("%Y-%m-%d")

    response = requests.get(f"https://syfak.gr/pharmacies_on_duty/search/{formatted_date}")
    if response.status_code == 200:
        pharmacy_data = {}
        soup = BeautifulSoup(response.content, "html.parser")
        data_table = soup.find("table", {"id": "dataTable"})
        data_table_body = data_table.find("tbody")
        rows = data_table_body.find_all("tr")
        i = 0
        for row in rows:
            columns = row.find_all("td")
            pharmacy_name = columns[1].text.strip()
            pharmacy_address = columns[2].text.strip()
            area = columns[3].text.strip()
            phone_number = columns[4].text.strip()
            start_time = columns[6].text.strip()
            end_time = columns[8].text.strip()
            directions = columns[9].a["href"]
            pharmacy_data[i] = {
                "pharmacy_name": pharmacy_name,
                "pharmacy_address": pharmacy_address,
                "area": area,
                "phone_number": phone_number,
                "timetable": f"{start_time} - {end_time}",
                "directions": directions
            }
            i += 1
        return pharmacy_data
    else:
        return {}
