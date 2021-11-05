from flask import Flask, render_template
from flask_restful import Api
from Pharmacies import PharmaciesToday, SpecificAreaPharmacy
from Hospitals import HospitalsToday

app = Flask(__name__)
api = Api(app)


@app.route('/')
def home():
    return render_template('index.html')


api.add_resource(PharmaciesToday.PharmacyInformation, '/pharmacies/today')
api.add_resource(SpecificAreaPharmacy.SpecificPharmaciesToday, '/pharmacies/specific_today')
api.add_resource(HospitalsToday.HospitalInformationToday, '/hospitals/today')

if __name__ == "__main__":
    app.run()
