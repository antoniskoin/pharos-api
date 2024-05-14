from flask import Flask, render_template, request
from waitress import serve
from scrapers.pharmacies import get_pharmacies_today, get_pharmacy_by_id, get_area_ids
from scrapers.hospitals import get_hospital_by_id, get_hospital_ids


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pharmacies/today", methods=["GET"])
def pharmacies_today():
    data = get_pharmacies_today()
    return data


@app.route("/pharmacies/area", methods=["GET"])
def pharmacies_in_area():
    area_id = request.args.get("id", None)
    data = get_pharmacy_by_id(area_id)
    return data


@app.route("/pharmacies/area-ids", methods=["GET"])
def pharmacies_area_ids():
    data = get_area_ids()
    return data


@app.route("/hospitals/area", methods=["GET"])
def hospitals_today():
    hospital_location = request.args.get("location", None)

    data = get_hospital_by_id(hospital_location)
    return data


@app.route("/hospitals/locations", methods=["GET"])
def hospital_locations():
    data = get_hospital_ids()
    return data


if __name__ == "__main__":
    serve(app)
