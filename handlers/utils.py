# handlers/utils.py

import datetime

def format_datetime(dt: datetime.datetime) -> str:
    """ارجع التاريخ والوقت بشكل مقروء عربي."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def mention_user(user):
    """ارجع منشن مستخدم تليجرام."""
    name = user.first_name
    return f"[{name}](tg://user?id={user.id})"

def is_admin(bot, chat_id, user_id):
    """تحقق هل المستخدم أدمن في المجموعة."""
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except Exception:
        return False

def is_owner(bot, chat_id, user_id, owners_list):
    """تحقق هل المستخدم مالك (من قائمة المالكين في البوت)."""
    return user_id in owners_list

def is_manager(managers_list, user_id):
    """تحقق هل المستخدم مدير (من قائمة المدراء في البوت)."""
    return user_id in managers_list

def clean_text(text):
    """إزالة الرموز الغريبة أو المسافات الزائدة من النص."""
    return ' '.join(text.split())

def get_chat_title(bot, chat_id):
    try:
        chat = bot.get_chat(chat_id)
        return chat.title or "مجموعة"
    except Exception:
        return "مجموعة"

def get_user_name(bot, user_id):
    try:
        user = bot.get_chat(user_id)
        return user.first_name
    except Exception:
        return "مستخدم"

def user_info(user):
    """ارجع معلومات المستخدم بنص منسق."""
    return f"الاسم: {user.first_name}\nالمعرف: @{user.username or 'لا يوجد'}\nID: {user.id}"