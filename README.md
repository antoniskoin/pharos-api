<p align="center">
  <img src="static/logo.png" width="110">
</p>

# Pharos API
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

#### An API that retrieves and returns data about pharmacies and hospitals that are on call in Greece.

## Supported Districts
- Athens
- Patra
- Crete

## Endpoints

```text
/pharmacies/today/<district> [GET]
```
Returns all pharmacies that are on duty in the specified district [Athens, Patra, Crete].

```text
/pharmacies/area [GET]
```
Returns all pharmacies that are on duty in the specified area.

```text
/pharmacies/area-ids [GET]
```
Returns the area IDs. Used with the **/pharmacies/area** endpoint.

```text
/hospitals/area [GET]
```
Returns all hospitals that are on duty in the specified area

```text
/hospitals/locations [GET]
```
Returns all hospital locations. Used with the **/hospitals/area** endpoint.