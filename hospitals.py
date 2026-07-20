import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def get_nearby_hospitals(latitude, longitude):

    query = f"""
    [out:json];
    (
      node
        ["amenity"="hospital"]
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

        hospitals = []

        for item in data["elements"]:

            name = item["tags"].get("name", "Noma'lum shifoxona")

            hospitals.append({
                "name": name,
                "lat": item["lat"],
                "lon": item["lon"]
            })

        return hospitals

    except Exception:
        return []
