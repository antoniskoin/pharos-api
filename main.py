from flask import Flask
from flask_restful import Api
from Pharmacies import PharmaciesToday, SpecificAreaPharmacy
from Hospitals import HospitalsToday

app = Flask(__name__)
api = Api(app)


api.add_resource(PharmaciesToday.PharmacyInformation, '/pharmacies/today')
api.add_resource(SpecificAreaPharmacy.SpecificPharmaciesToday, '/pharmacies/specific_today')
api.add_resource(HospitalsToday.HospitalInformationToday, '/hospitals/today')

if __name__ == "__main__":
    app.run()
