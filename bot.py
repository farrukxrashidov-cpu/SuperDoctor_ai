from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from ai import ask_ai
from config import BOT_TOKEN

MENU = [
    ["🤖 AI Shifokor", "🚑 Birinchi yordam"],
    ["🏥 Kasalliklar", "💊 Dorilar"],
    ["📍 Yaqin shifoxona", "💊 Yaqin dorixona"],
    ["❤️ BMI", "💧 Suv kalkulyatori"],
    ["ℹ️ Bot haqida"]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(
        MENU,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "👋 SuperDoctor_AI ga xush kelibsiz!\n\n"
        "⚠️ Muhim: Bu bot shifokor o'rnini bosmaydi. "
        "U faqat umumiy ma'lumot va tavsiyalar beradi.\n\n"
        "Kerakli bo'limni tanlang.",
        reply_markup=keyboard
    )


async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "ℹ️ Bot haqida":
        await update.message.reply_text(
            "SuperDoctor_AI\n"
            "AI tibbiy yordamchi."
        )
        return

    answer = ask_ai(text)

    await update.message.reply_text(answer)


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

print("✅ SuperDoctor_AI ishga tushdi...")

app.run_polling()
