import requests
import datetime

from bs4 import BeautifulSoup
from flask import request
from requests import Session

from helpers.common import get_headers


def get_pharmacies_today() -> dict:
    pharmacy_information = {}

    response = requests.get("https://fsa-efimeries.gr/", headers=get_headers())

    if response.status_code != 200:
        return {"success": False, "error": f"Request failed with status code {response.status_code}"}

    soup = BeautifulSoup(response.content, "html.parser")
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
            return {"success": False, "error": f"{error}"}

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


def get_area_ids() -> dict:
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
        return {}


def get_pharmacy_by_id(area: str) -> dict:
    if not area.isdigit():
        return {"error": "Area ID must be a digit"}

    specific_area_info = {}
    session = Session()
    response = session.get("https://fsa-efimeries.gr/", headers=get_headers())

    if response.status_code != 200:
        return {"success": False, "error": f"Request failed with status code {response.status_code}"}

    verification_cookie = response.cookies.get(".AspNetCore.Antiforgery._7w_lBqvcBI")
    date_today = datetime.datetime.now()
    formatted_date = date_today.strftime("%Y-%m-%d")
    data = {
        "Date": formatted_date,
        "PerioxiId": int(area),
        "isOpen": "false",
        "__RequestVerificationToken": verification_cookie,
        "IsOpen": "false"
    }
    response = session.post("https://fsa-efimeries.gr/", data=data, headers=get_headers())

    if response.status_code != 200:
        return {"success": False, "error": f"Request failed with status code {response.status_code}"}

    soup = BeautifulSoup(response.content, "html.parser")
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
            return {"success": False, "error": f"An error occurred: {error}"}

        if status:
            status = "OPEN"
        else:
            status = "CLOSED"

        specific_area_info[pharmacy_count] = {
            "pharmacy": pharmacy,
            "area": area,
            "address": address,
            "phone": phone,
            "timetable": timetable,
            "status": status
        }

        pharmacy_count += 1

    return specific_area_info
