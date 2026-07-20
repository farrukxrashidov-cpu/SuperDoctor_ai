import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def get_nearby_pharmacies(latitude, longitude):

    query = f"""
    [out:json];
    (
      node
        ["amenity"="pharmacy"]
        (around:5000,{latitude},{longitude});
    );
    out;
    """

    try:
        response = requests.get(
            OVERPASS_URL,
            params={"data": query},
            timeout=20
        )

        data = response.json()

        pharmacies = []

        for item in data["elements"]:

            name = item["tags"].get(
                "name",
                "Noma'lum dorixona"
            )

            pharmacies.append({
                "name": name,
                "lat": item["lat"],
                "lon": item["lon"]
            })

        return pharmacies

    except Exception:
        return []
