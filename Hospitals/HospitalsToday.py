import requests
import datetime
from bs4 import BeautifulSoup
from flask_restful import Resource
from flask import request
from helpers.common import get_headers


class HospitalInformationToday(Resource):
    def get(self):
        clinic_requested = request.args.get("clinic")
        area_requested = request.args.get("area")
        hospital_info = {}
        date_today = datetime.datetime.now()
        formatted_date = date_today.strftime("%w/%m/%Y")
        url = f"https://www.xo.gr/efimerevonta-nosokomeia/{area_requested}/?date={formatted_date}&clinic={clinic_requested}"
        req = requests.get(url, headers=get_headers())

        if req.status_code != 200:
            return f"Request failed with status code {req.status_code}"

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
