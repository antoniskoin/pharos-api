import requests
from bs4 import BeautifulSoup
from flask_restful import Resource


class HospitalInformationToday(Resource):
    def get(self):
        keys = ["Όλες", "Αγγειοχειρουργική", "Αιματολογική", "Αιμοδοσία", "Γαστρεντερολογική", "Γενική Εφημερία",
                "Γναθοχειρουργική", "Γυναικολογική", "Δερματολογική", "Διαβητολογικό Κέντρο", "Ενδοκρινολογική",
                "Θωρακοχειρουργική", "Καρδιολογική", "Καρδιολογική (αιμοδυναμικό εργαστήριο)", "Καρδιοχειρουργική",
                "Κλινική Χεριού", "Μαιευτική", "ΜΕΘ Νεογνών", "Νεογνολογικό", "Νευρολογική", "Νευροχειρουργική",
                "Νεφρολογική", "Ογκολογική", "Οδοντιατρική", "Ορθοπεδική", "Ουρολογική", "Οφθαλμολογική", "Παθολογική",
                "Παιδιατρικό", "Παιδοαιματολογική", "Παιδονεφρολογική", "Παιδοορθοπαιδική",
                "Παιδοορθοπεδική-Παιδοχειρουργική", "Παιδοχειρουργική", "Παιδοψυχιατρική", "Παιδοψυχιατρικό",
                "Παιδο-ΩΡΛ", "Πλαστική Χειρουργική", "Πνευμονολογική", "Ρευματολογική", "Χειρουργική", "Ψυχιατρική",
                "ΩΡΛ"]

        hospital_info = {}

        url = "https://www.xo.gr/efimerevonta-nosokomeia/athina/?date=03/11/2021"
        req = requests.get(url)
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
