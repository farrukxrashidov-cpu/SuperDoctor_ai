from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN
from ai import ask_ai
from database import add_user
from first_aid import get_topics, get_first_aid
from hospitals import get_nearby_hospitals
from pharmacy import get_nearby_pharmacies
from medicines import get_medicine
from diseases import get_disease
from profile import get_profile
from bmi import calculate_bmi
from water import calculate_water


MENU = [
    ["🤖 AI Shifokor", "🚑 Birinchi yordam"],
    ["🏥 Kasalliklar", "💊 Dorilar"],
    ["📍 Shifoxona", "💊 Dorixona"],
    ["❤️ BMI", "💧 Suv"],
    ["👤 Profil", "🆘 SOS"],
    ["ℹ️ Bot haqida"]
]

LOCATION_BUTTON = ReplyKeyboardMarkup(
    [[KeyboardButton("📍 Lokatsiyani yuborish", request_location=True)]],
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.full_name, user.username)

    context.user_data["mode"] = None

    keyboard = ReplyKeyboardMarkup(MENU, resize_keyboard=True)

    await update.message.reply_text(
        "👨‍⚕️ SuperDoctor_AI ga xush kelibsiz!\n\n"
        "Kerakli bo'limni tanlang.",
        reply_markup=keyboard
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # ===== Profil =====
    if text == "👤 Profil":
        await update.message.reply_text(get_profile(update.effective_user))
        return

    # ===== AI Shifokor =====
    if text == "🤖 AI Shifokor":
        await update.message.reply_text(
            "🩺 Alomatlaringizni yozing.\n\n"
            "Masalan:\n"
            "3 kundan beri tomog'im og'riyapti va isitmam bor."
        )
        context.user_data["mode"] = "ai"
        return

    # ===== Birinchi yordam =====
    if text == "🚑 Birinchi yordam":
        keyboard = [[i] for i in get_topics()]
        keyboard.append(["🔙 Orqaga"])
        await update.message.reply_text(
            "Kerakli holatni tanlang.",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    if text in get_topics():
        await update.message.reply_text(get_first_aid(text))
        return

    # ===== Kasalliklar =====
    if text == "🏥 Kasalliklar":
        await update.message.reply_text(
            "🔍 Kasallik nomini yozing.\n\nMasalan:\nGripp"
        )
        context.user_data["mode"] = "disease"
        return

    # ===== Dorilar =====
    if text == "💊 Dorilar":
        await update.message.reply_text(
            "💊 Dori nomini yozing.\n\nMasalan:\nParacetamol"
        )
        context.user_data["mode"] = "medicine"
        return

    # ===== Shifoxona (lokatsiya so'raladi) =====
    if text == "📍 Shifoxona":
        context.user_data["mode"] = "hospital"
        await update.message.reply_text(
            "📍 Eng yaqin shifoxonalarni topish uchun lokatsiyangizni yuboring.",
            reply_markup=LOCATION_BUTTON
        )
        return

    # ===== Dorixona (lokatsiya so'raladi) =====
    if text == "💊 Dorixona":
        context.user_data["mode"] = "pharmacy"
        await update.message.reply_text(
            "📍 Eng yaqin dorixonalarni topish uchun lokatsiyangizni yuboring.",
            reply_markup=LOCATION_BUTTON
        )
        return

    # ===== BMI =====
    if text == "❤️ BMI":
        await update.message.reply_text(
            "❤️ BMI kalkulyatori\n\n"
            "Quyidagi formatda yuboring:\n\n"
            "70 175\n\n"
            "(Vazn kg va bo'y sm)"
        )
        context.user_data["mode"] = "bmi"
        return

    # ===== Suv =====
    if text == "💧 Suv":
        await update.message.reply_text(
            "💧 Vazningizni kiriting.\n\nMasalan:\n70"
        )
        context.user_data["mode"] = "water"
        return

    # ===== SOS =====
    if text == "🆘 SOS":
        await update.message.reply_text(
            "🚨 Agar bemor:\n\n"
            "• Nafas olmayotgan bo'lsa\n"
            "• Hushsiz bo'lsa\n"
            "• Kuchli qon ketayotgan bo'lsa\n"
            "• Ko'krakda kuchli og'riq bo'lsa\n\n"
            "Darhol tez yordamga qo'ng'iroq qiling!"
        )
        return

    # ===== Bot haqida =====
    if text == "ℹ️ Bot haqida":
        await update.message.reply_text(
            "👨‍⚕️ SuperDoctor_AI\n\n"
            "Sun'iy intellekt yordamida ishlovchi tibbiy yordamchi."
        )
        return

    # ===== Orqaga =====
    if text == "🔙 Orqaga":
        await start(update, context)
        return

    mode = context.user_data.get("mode")

    # ===== AI rejimi =====
    if mode == "ai":
        answer = ask_ai(text)
        await update.message.reply_text(answer)
        return

    # ===== Kasallik qidirish =====
    if mode == "disease":
        disease = get_disease(text)
        if disease:
            await update.message.reply_text(str(disease))
        else:
            await update.message.reply_text("❌ Kasallik topilmadi.")
        return

    # ===== Dori qidirish =====
    if mode == "medicine":
        medicine = get_medicine(text)
        if medicine:
            await update.message.reply_text(str(medicine))
        else:
            await update.message.reply_text("❌ Dori topilmadi.")
        return

    # ===== BMI hisoblash =====
    if mode == "bmi":
        try:
            weight_str, height_str = text.split()
            weight = float(weight_str)
            height = float(height_str)
            result = calculate_bmi(weight, height)
            await update.message.reply_text(str(result))
        except ValueError:
            await update.message.reply_text(
                "❌ Format xato. Masalan: 70 175"
            )
        context.user_data["mode"] = None
        return

    # ===== Suv hisoblash =====
    if mode == "water":
        try:
            weight = float(text)
            result = calculate_water(weight)
            await update.message.reply_text(str(result))
        except ValueError:
            await update.message.reply_text("❌ Format xato. Masalan: 70")
        context.user_data["mode"] = None
        return

    await update.message.reply_text("Iltimos, menyudan bo'lim tanlang.")


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    mode = context.user_data.get("mode")

    await update.message.reply_text(
        f"📍 Lokatsiya qabul qilindi.\n\n"
        f"Latitude: {latitude}\n"
        f"Longitude: {longitude}\n\n"
        "🔎 Qidirilmoqda..."
    )

    if mode == "pharmacy":
        results = get_nearby_pharmacies(latitude, longitude)
    else:
        results = get_nearby_hospitals(latitude, longitude)

    await update.message.reply_text(str(results))
    context.user_data["mode"] = None


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, location))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ SuperDoctor_AI ishga tushdi.")
    app.run_polling()


if __name__ == "__main__":
    main()
