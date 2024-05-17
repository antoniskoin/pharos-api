import requests
from bs4 import BeautifulSoup
from datetime import datetime


def parse_time_string(time_range: str):
    time_range = time_range.lower().replace("μμ", "").replace("πμ", "").strip()
    start_time_str, end_time_str = time_range.split(" - ")

    start_time = datetime.strptime(start_time_str.strip(), "%H:%M").time()
    end_time = datetime.strptime(end_time_str.strip(), "%H:%M").time()
    return start_time, end_time


def get_patra_pharmacies_today() -> dict:
    url = "https://www.efimeria.gr"
    response = requests.get(url, headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"})
    if response.status_code == 200:
        pharmacy_data = {}
        soup = BeautifulSoup(response.content, "html.parser")
        duties_container = soup.find("div", {"id": "all_duties"})
        duties_body = duties_container.find("div", {"class": "panel-body"})
        bg_primaries = duties_body.find_all("div", {"class": "row bg-primary"})
        bg_row = duties_body.find_all(lambda tag: tag.name == "div" and tag["class"] == ["row"])
        i = 0
        counter = 0
        for row in bg_primaries:
            open_hours = row.text.strip()
            start, end = parse_time_string(open_hours)

            pharmacy_container = bg_row[i]
            pharmacies = pharmacy_container.find_all("div", {"class": "col-xs-12 col-md-6"})
            if len(pharmacies) == 0:
                pharmacies = pharmacy_container.find_all("div", {"class": "col-xs-12 col-md-12"})

            for pharmacy in pharmacies:
                pharmacy_name = pharmacy.find("span", {"class": "pharmacy_name"}).text.strip()
                pharmacy_address = pharmacy.find("span", {"class": "pharmacy_address"}).text.strip()
                pharmacy_data[counter] = {
                    "pharmacy": pharmacy_name,
                    "area": "ΠΑΤΡΑ",
                    "address": pharmacy_address,
                    "phone": None,
                    "timetable": f"{start} - {end}",
                    "status": None
                }
            i += 1
            counter += 1
        return pharmacy_data
    else:
        return {}
