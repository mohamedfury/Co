from telebot.types import ChatMember, Message
import os
import json

DATA_DIR = "data"
ROLES_FILE = os.path.join(DATA_DIR, "roles.json")

def get_role(chat_id, user_id):
    """جلب الرتبة المخصصة من ملف roles.json"""
    if not os.path.exists(ROLES_FILE):
        return None
    with open(ROLES_FILE, encoding="utf-8") as f:
        try:
            roles = json.load(f)
        except Exception:
            return None
    return roles.get(str(chat_id), {}).get(str(user_id), None)

def is_owner(chat_member: ChatMember):
    """هل العضو هو مالك المجموعة؟"""
    return chat_member.status == "creator"

def is_admin(chat_member: ChatMember):
    """هل العضو أدمن أو مالك؟"""
    return chat_member.status in ["administrator", "creator"]

def is_member(chat_member: ChatMember):
    """هل العضو عضو عادي؟"""
    return chat_member.status == "member"

def is_restricted(chat_member: ChatMember):
    """هل العضو مقيّد؟"""
    return chat_member.status == "restricted"

def is_banned(chat_member: ChatMember):
    """هل العضو محظور؟"""
    return chat_member.status == "kicked"

def is_bot(user):
    """هل العضو بوت؟"""
    return getattr(user, "is_bot", False)

# مثال دوال مع رتبك المخصصة
def is_custom_role(chat_id, user_id, role_name):
    """هل لدى العضو رتبة معيّنة من roles.json؟"""
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
    """دالة تحقق هل العضو يملك صلاحية أو رتبة تسمح باستخدام أوامر الأدمن"""
    chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
    # يمكنك تخصيص الشروط حسب نظامك
    if is_admin(chat_member) or is_owner(chat_member):
        return True
    # أو لو عنده رتبة مخصصة
    role = get_role(message.chat.id, message.from_user.id)
    return role in ["مدير", "منشئ", "مالك"]

# مثال: استدعاء صلاحية في هاندلر
# from utils import permissions
# if not permissions.can_use_admin_cmds(bot, message):
#     return bot.reply_to(message, "❗️ ليس لديك صلاحية تنفيذ هذا الأمر.")
