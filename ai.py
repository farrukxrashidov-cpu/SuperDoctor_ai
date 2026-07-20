from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Siz SuperDoctor_AI nomli tibbiy yordamchisiz.

Qoidalar:
- Hech qachon aniq tashxis qo'ymang.
- Faqat umumiy tibbiy ma'lumot va tavsiyalar bering.
- Xavfli alomatlar bo'lsa darhol shifokorga yoki tez yordamga murojaat qilishni tavsiya qiling.
- Javoblarni o'zbek tilida yozing.
- Qisqa va tushunarli javob bering.
"""

def ask_ai(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Xatolik: {e}"
