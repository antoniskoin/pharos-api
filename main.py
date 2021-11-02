from flask import Flask
from flask_restful import Api
from Pharmacies import PharmaciesToday

app = Flask(__name__)
api = Api(app)


api.add_resource(PharmaciesToday.PharmacyInformation, '/pharmacies/today')

if __name__ == "__main__":
    app.run()
