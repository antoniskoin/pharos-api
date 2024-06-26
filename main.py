from flask import Flask, render_template, request
from waitress import serve
from scrapers.athens import get_pharmacies_today, get_pharmacy_by_id, get_area_ids
from scrapers.patra import get_patra_pharmacies_today
from scrapers.crete import get_crete_pharmacies_today
from scrapers.hospitals import get_hospital_by_id, get_hospital_ids

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pharmacies/today/<district>", methods=["GET"])
def pharmacies_today(district: str):
    if district.lower() == "athens":
        data = get_pharmacies_today()
    elif district.lower() == "patra":
        data = get_patra_pharmacies_today()
    elif district.lower() == "crete":
        data = get_crete_pharmacies_today()
    else:
        return {"error": "invalid district"}

    return data


@app.route("/pharmacies/area", methods=["GET"])
def pharmacies_in_area():
    area_id = request.args.get("id", None)

    if not area_id:
        return {"success": False, "message": "No area id provided"}

    data = get_pharmacy_by_id(area_id)
    return data


@app.route("/pharmacies/area-ids", methods=["GET"])
def pharmacies_area_ids():
    data = get_area_ids()
    return data


@app.route("/hospitals/area", methods=["GET"])
def hospitals_today():
    hospital_location = request.args.get("location", None)

    if not hospital_location:
        return {"success": False, "message": "No location provided"}

    data = get_hospital_by_id(hospital_location)
    return data


@app.route("/hospitals/locations", methods=["GET"])
def hospital_locations():
    data = get_hospital_ids()
    return data


if __name__ == "__main__":
    serve(app)
