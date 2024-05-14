import datetime
import requests
from helpers.common import get_headers
from bs4 import BeautifulSoup


def get_hospital_by_id(area_requested: str) -> dict:
    if not area_requested:
        return {"error": "No area was specified"}

    hospital_info = {}
    date_today = datetime.datetime.now()
    formatted_date = date_today.strftime("%d/%m/%Y")
    url = f"https://www.xo.gr/efimerevonta-nosokomeia/{area_requested}/?date={formatted_date}"
    req = requests.get(url, headers=get_headers())

    if req.status_code != 200:
        return {"success": False, "error": f"Request failed with status code {req.status_code}"}

    soup = BeautifulSoup(req.content, "html.parser")
    search_results = soup.find("div", {"id": "SearchResults"})
    items = search_results.find_all("div", {"class": "basicInfo"})
    hospital_count = 0
    for item in items:
        hospital = item.find("a", {"class": "et-v2"}).text.replace("ΤΗΛΕΦΩΝΙΚΟ ΚΕΝΤΡΟ - ", "")
        sub_category = item.find("div", {"class": "listingGreyArea"})
        clinics = sub_category.find("span", {"class": "clinic"}).text

        address_info = item.find("p", {"class": "listingAddressInfo"})
        address = address_info.find("span", {"itemprop": "streetAddress"}).text
        try:
            district = address_info.find("span", {"class": "district"}).text
        except AttributeError:
            district = "N/A"

        postal_code = address_info.find("span", {"itemprop": "postalCode"}).text
        locality = address_info.find("span", {"itemprop": "addressLocality"}).text
        region = address_info.find("span", {"itemprop": "addressRegion"}).text

        hospital_info[hospital_count] = {
            "hospital": hospital,
            "clinics": clinics,
            "address": address,
            "district": district,
            "postal_code": postal_code,
            "locality": locality,
            "region": region
        }

        hospital_count += 1

    return hospital_info


def get_hospital_ids() -> dict:
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
            areas[i] = area
            i += 1

        return areas
    else:
        return {"success": False}
