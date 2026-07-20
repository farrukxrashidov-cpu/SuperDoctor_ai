import json

with open("data/medicines.json", "r", encoding="utf-8") as f:
    MEDICINES = json.load(f)


def get_medicine(name):
    return MEDICINES.get(name.lower())


def search_medicine(keyword):
    keyword = keyword.lower()

    result = []

    for medicine in MEDICINES:

        if keyword in medicine:

            result.append(medicine)

    return result[:10]
