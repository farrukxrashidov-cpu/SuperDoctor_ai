MEDICINES = {
    "paracetamol": {
        "foydalanish": "Isitma va og'riqni kamaytiradi.",
        "ogohlantirish": "Dozani oshirmang."
    },
    "ibuprofen": {
        "foydalanish": "Og'riq va yallig'lanishga qarshi.",
        "ogohlantirish": "Oshqozon yarasi bo'lsa ehtiyot bo'ling."
    }
}

def get_medicine(name):
    return MEDICINES.get(name.lower())
