from telebot.types import ChatMember, Message
import os
import json

DATA_DIR = "data"
ROLES_FILE = os.path.join(DATA_DIR, "roles.json")

def get_role(chat_id, user_id):
    """جلب الرتبة المخصصة من ملف roles.json"""
    if not os.path.exists(ROLES_FILE):
        return "عضو"
    try:
        with open(ROLES_FILE, encoding="utf-8") as f:
            roles = json.load(f)
    except Exception:
        return "عضو"
    return roles.get(str(chat_id), {}).get(str(user_id), "عضو")

def is_owner(chat_member: ChatMember):
    """هل العضو هو مالك المجموعة؟"""
    if chat_member is None:
        return False
    return chat_member.status == "creator"

def is_admin(chat_member: ChatMember):
    """هل العضو أدمن أو مالك؟"""
    if chat_member is None:
        return False
    return chat_member.status in ["administrator", "creator"]

def is_member(chat_member: ChatMember):
    """هل العضو عضو عادي؟"""
    if chat_member is None:
        return False
    return chat_member.status == "member"

def is_restricted(chat_member: ChatMember):
    """هل العضو مقيّد؟"""
    if chat_member is None:
        return False
    return chat_member.status == "restricted"

def is_banned(chat_member: ChatMember):
    """هل العضو محظور؟"""
    if chat_member is None:
        return False
    return chat_member.status == "kicked"

def is_bot(user):
    """هل العضو بوت؟"""
    return getattr(user, "is_bot", False)

# رتب مخصصة من roles.json
def is_custom_role(chat_id, user_id, role_name):
    role = get_role(chat_id, user_id)
    return role == role_name

def is_vip(chat_id, user_id):
    return is_custom_role(chat_id, user_id, "مميز")

def is_manager(chat_id, user_id):
    return is_custom_role(chat_id, user_id, "مدير")

def is_creator(chat_id, user_id):
    return is_custom_role(chat_id, user_id, "منشئ")

def is_main_owner(chat_id, user_id):
    return is_custom_role(chat_id, user_id, "مالك")

def can_use_admin_cmds(bot, message: Message):
    """تحقق إذا العضو يمكنه استخدام أوامر الأدمن"""
    try:
        chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
    except Exception:
        return False
    if is_admin(chat_member) or is_owner(chat_member):
        return True
    role = get_role(message.chat.id, message.from_user.id)
    return role in ["مدير", "منشئ", "مالك"]

# مثال استدعاء داخل الهاندلر:
# if not can_use_admin_cmds(bot, message):
#     return bot.reply_to(message, "❗️ ليس لديك صلاحية تنفيذ هذا الأمر.")
