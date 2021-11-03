from flask import Flask
from flask_restful import Api
from Pharmacies import PharmaciesToday
from Hospitals import HospitalsToday

app = Flask(__name__)
api = Api(app)


api.add_resource(PharmaciesToday.PharmacyInformation, '/pharmacies/today')
api.add_resource(HospitalsToday.HospitalInformationToday, '/hospitals/today')

if __name__ == "__main__":
    app.run()
