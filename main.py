from flask import Flask, render_template
from flask_restful import Api
from Pharmacies import pharmacies_today, specific_area_pharmacy
from Hospitals import hospitals_today

app = Flask(__name__)
api = Api(app)


@app.route("/")
def home():
    return render_template("index.html")


api.add_resource(pharmacies_today.PharmacyInformation, "/pharmacies/today")
api.add_resource(specific_area_pharmacy.SpecificPharmaciesToday, "/pharmacies/specific_today")
api.add_resource(hospitals_today.HospitalInformationToday, "/hospitals/today")

if __name__ == "__main__":
    app.run()
