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
from pharmacy import get_nearby_pharmacies
from hospitals import get_nearby_hospitals
from profile import get_profile
MENU = [
    ["🤖 AI Shifokor", "🚑 Birinchi yordam"],
    ["🏥 Kasalliklar", "💊 Dorilar"],
    ["📍 Shifoxona", "💊 Dorixona"],
    ["❤️ BMI", "💧 Suv"],
    ["🆘 SOS", "ℹ️ Bot haqida"]
]

LOCATION_BUTTON = ReplyKeyboardMarkup(
    [[KeyboardButton("📍 Lokatsiyani yuborish", request_location=True)]],
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    add_user(
        user.id,
        user.full_name,
        user.username
    )

    keyboard = ReplyKeyboardMarkup(
        MENU,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "👨‍⚕️ SuperDoctor_AI ga xush kelibsiz!\n\n"
        "Kerakli bo'limni tanlang.",
        reply_markup=keyboard
    )
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # AI
    if text == "🤖 AI Shifokor":
        await update.message.reply_text(
            "🩺 Alomatlaringizni yozing.\n\n"
            "Masalan:\n"
            "3 kundan beri tomog'im og'riyapti va isitmam bor."
        )
        context.user_data["mode"] = "ai"
        return

    # Birinchi yordam
    if text == "🚑 Birinchi yordam":

        keyboard = [[i] for i in get_topics()]

        keyboard.append(["🔙 Orqaga"])

        await update.message.reply_text(
            "Kerakli holatni tanlang.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )
        return

    # SOS
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

    # Bot haqida
    if text == "ℹ️ Bot haqida":

        await update.message.reply_text(
            "👨‍⚕️ SuperDoctor_AI\n\n"
            "Sun'iy intellekt yordamida ishlovchi tibbiy yordamchi."
        )

        return

    # Orqaga
    if text == "🔙 Orqaga":

        await start(update, context)

        return

    # Birinchi yordam mavzulari
    if text in get_topics():

        await update.message.reply_text(
            get_first_aid(text)
        )

        return

    # AI rejimi
    if context.user_data.get("mode") == "ai":

        answer = ask_ai(text)

        await update.message.reply_text(answer)

        return

    await update.message.reply_text(
        "Iltimos, menyudan bo'lim tanlang."
        )
    # ====== LOCATION ======

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):

    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    await update.message.reply_text(
        f"📍 Lokatsiya qabul qilindi.\n\n"
        f"Latitude: {latitude}\n"
        f"Longitude: {longitude}\n\n"
        "🔎 Sizga eng yaqin shifoxona va dorixonalarni qidirmoqdaman..."
    )

    # Keyin hospitals.py va pharmacy.py orqali haqiqiy qidiruv qilamiz.


# ====== BMI ======

async def bmi(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "❤️ BMI kalkulyatori\n\n"
        "Quyidagi formatda yuboring:\n\n"
        "70 175\n\n"
        "(Vazn kg va bo'y sm)"
    )

    context.user_data["mode"] = "bmi"


# ====== WATER ======

async def water(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "💧 Vazningizni kiriting.\n\n"
        "Masalan:\n70"
    )

    context.user_data["mode"] = "water"


# ====== APPLICATION ======

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(MessageHandler(filters.LOCATION, location))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # SHU YERGA MEN YUBORGAN BMI VA SUV KODINI QO'YASAN

    if text == "❤️ BMI":
        ...

    if text == "💧 Suv":
        ...

    # KEYIN ESA OLDINGI KODLAR DAVOM ETADI
print("✅ SuperDoctor_AI ishga tushdi.")
# Kasallik qidirish
if text == "🏥 Kasalliklar":

    await update.message.reply_text(
        "🔍 Kasallik nomini yozing.\n\n"
        "Masalan:\nGripp"
    )

    context.user_data["mode"] = "disease"
    return


# Dori qidirish
if text == "💊 Dorilar":

    await update.message.reply_text(
        "💊 Dori nomini yozing.\n\n"
        "Masalan:\nParacetamol"
    )

    context.user_data["mode"] = "medicine"
    return


# Kasallik ma'lumotlari
if context.user_data.get("mode") == "disease":

    disease = get_disease(text)

    if disease:
        await update.message.reply_text(str(disease))
    else:
        await update.message.reply_text(
            "❌ Kasallik topilmadi."
        )

    return


# Dori ma'lumotlari
if context.user_data.get("mode") == "medicine":

    medicine = get_medicine(text)

    if medicine:
        await update.message.reply_text(str(medicine))
    else:
        await update.message.reply_text(
            "❌ Dori topilmadi."
        )

    return 
app.run_polling()
from bmi import calculate_bmi
from water import calculate_water
from medicines import get_medicine
from diseases import get_disease
