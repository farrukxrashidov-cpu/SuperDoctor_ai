def calculate_bmi(weight, height):

    height = height / 100
    bmi = weight / (height * height)

    if bmi < 18.5:
        status = "Ozg'in"

    elif bmi < 25:
        status = "Normal"

    elif bmi < 30:
        status = "Ortiqcha vazn"

    else:
        status = "Semizlik"

    return round(bmi, 1), status
