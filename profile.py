from database import get_users_count

def get_profile(user):

    text = f"""
👤 Profil

🆔 ID: {user.id}

👤 Ism:
{user.full_name}

📛 Username:
@{user.username}

📊 Jami foydalanuvchilar:
{get_users_count()}
"""

    return text
