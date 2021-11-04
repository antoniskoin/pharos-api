import requests
import datetime
from bs4 import BeautifulSoup
from flask_restful import Resource
from flask import request
from helpers.common import get_user_agent


class HospitalInformationToday(Resource):
    def get(self):
        clinic_requested = request.args.get("clinic")
        hospital_info = {}
        date_today = datetime.datetime.now()
        formatted_date = date_today.strftime("%w/%m/%Y")
        url = f"https://www.xo.gr/efimerevonta-nosokomeia/athina/?date={formatted_date}&clinic={clinic_requested}"
        req = requests.get(url, headers={"user-agent": get_user_agent()})
        soup = BeautifulSoup(req.content, "html.parser")
        search_results = soup.find("div", {"id": "SearchResults"})
        items = search_results.find_all("div", {"class": "basicInfo"})
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

            hospital_info[hospital] = {
                "clinics": clinics,
                "address": address,
                "district": district,
                "postal_code": postal_code,
                "locality": locality,
                "region": region
            }

        return hospital_info
