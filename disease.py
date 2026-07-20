import json

with open("data/diseases.json", "r", encoding="utf-8") as f:
    DISEASES = json.load(f)


def get_disease(name):
    return DISEASES.get(name.lower())


def search_disease(keyword):
    keyword = keyword.lower()

    result = []

    for disease in DISEASES:

        if keyword in disease:

            result.append(disease)

    return result[:10]
