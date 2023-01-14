from flask import Flask, render_template
from flask_restful import Api
from Pharmacies import pharmacies_today, specific_area_pharmacy, get_area_ids
from Hospitals import hospitals_today, get_hospital_locations
from waitress import serve


app = Flask(__name__)
api = Api(app)


@app.route("/")
def home():
    return render_template("index.html")


api.add_resource(pharmacies_today.PharmacyInformation, "/pharmacies/today")
api.add_resource(specific_area_pharmacy.SpecificPharmaciesToday, "/pharmacies/specific_today")
api.add_resource(get_area_ids.AreaID, "/pharmacies/get_area_ids")
api.add_resource(hospitals_today.HospitalInformationToday, "/hospitals/today")
api.add_resource(get_hospital_locations.Locations, "/hospitals/get_hospital_locations")


if __name__ == "__main__":
    serve(app)
