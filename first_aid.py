FIRST_AID = {

    "❤️ Yurak xuruji":
"""
🚨 Yurak xuruji

Belgilar:
• Ko'krakda kuchli og'riq
• Chap qo'l yoki jag'ga tarqaluvchi og'riq
• Nafas qisishi
• Sovuq ter

Birinchi yordam:
1. Darhol tez yordam chaqiring.
2. Bemorni o'tqazing yoki yotqizing.
3. Tor kiyimlarini bo'shating.
4. Hushidan ketsa CPR boshlang.

❌ Nima qilmaslik kerak:
• Bemorni yugurtirmang.
""",

    "🧠 Insult":
"""
🚨 Insult

Belgilar:
• Yuzning bir tomoni osilishi
• Qo'l yoki oyoq kuchsizligi
• Gapira olmaslik

Birinchi yordam:
1. Darhol tez yordam chaqiring.
2. Bemorni xavfsiz joyga yotqizing.
3. Ovqat yoki suv bermang.

❌ Kechiktirmang.
""",

    "🩸 Kuchli qon ketishi":
"""
🚨 Kuchli qon ketishi

1. Toza mato bilan bosim bering.
2. Jarohatni balandroq tuting.
3. Qon to'xtamasa tez yordam chaqiring.

❌ Turniketni noto'g'ri ishlatmang.
""",

    "🔥 Kuyish":
"""
🔥 Kuyish

1. Kuygan joyni 20 daqiqa salqin suvda ushlang.
2. Toza bint bilan yoping.

❌ Muz qo'ymang.
❌ Yog' yoki tish pastasi surtmang.
""",

    "😵 Hushdan ketish":
"""
😵 Hushdan ketish

1. Oyoqlarini biroz ko'taring.
2. Nafas olayotganini tekshiring.
3. Hushiga kelmasa tez yordam chaqiring.
"""
}


def get_first_aid(topic):
    return FIRST_AID.get(
        topic,
        "❌ Bu mavzu hali bazaga qo'shilmagan."
    )


def get_topics():
    return list(FIRST_AID.keys())
