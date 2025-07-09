import json
import os
from telebot.types import Message, InputMediaPhoto

DATA = "data"
USERS_FILE = os.path.join(DATA, "users.json")
ROLES_FILE = os.path.join(DATA, "roles.json")

# دالة مساعدة: تحميل بيانات الأعضاء
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {}

# دالة مساعدة: حفظ بيانات الأعضاء
def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# دالة جلب عدد الرسائل
def get_messages_count(user_id, chat_id):
    users = load_users()
    return users.get(str(chat_id), {}).get(str(user_id), {}).get("messages", 0)

# دالة جلب النقاط
def get_points(user_id, chat_id):
    users = load_users()
    return users.get(str(chat_id), {}).get(str(user_id), {}).get("points", 0)

# دالة تحديث عداد الرسائل
def increment_messages(user_id, chat_id):
    users = load_users()
    chat_users = users.setdefault(str(chat_id), {})
    user_data = chat_users.setdefault(str(user_id), {})
    user_data["messages"] = user_data.get("messages", 0) + 1
    save_users(users)

# دالة جلب الرتبة
def get_role(user_id, chat_id):
    if not os.path.exists(ROLES_FILE):
        return "عضو"
    with open(ROLES_FILE, encoding="utf-8") as f:
        try:
            roles = json.load(f)
        except Exception:
            return "عضو"
    return roles.get(str(chat_id), {}).get(str(user_id), "عضو")

# دالة جلب معلومات العضو
def get_user_info(bot, user, chat_id):
    msg_count = get_messages_count(user.id, chat_id)
    points = get_points(user.id, chat_id)
    role = get_role(user.id, chat_id)
    return (
        f"👤 الاسم: {user.first_name or ''}\n"
        f"🆔 آيدي: `{user.id}`\n"
        f"🏷 اسم المستخدم: @{user.username if user.username else 'لا يوجد'}\n"
        f"⭐️ الرتبة: {role}\n"
        f"💬 رسائل: {msg_count}\n"
        f"🌟 نقاط: {points}"
    )

# ----------- تسجيل أوامر الأعضاء -----------
def register(bot):
    # زيادة عداد الرسائل لكل رسالة عضو (يمكنك تخصيصه أكثر)
    @bot.message_handler(func=lambda m: m.chat.type in ["group", "supergroup"])
    def count_member_messages(message: Message):
        if not message.from_user.is_bot:
            increment_messages(message.from_user.id, message.chat.id)

    @bot.message_handler(commands=["معرفي", "id"])
    def my_id(message: Message):
        user = message.from_user
        bot.reply_to(message, f"آيديك: `{user.id}`", parse_mode="Markdown")

    @bot.message_handler(commands=["رسائلي"])
    def my_messages(message: Message):
        count = get_messages_count(message.from_user.id, message.chat.id)
        bot.reply_to(message, f"عدد رسائلك هنا: {count}")

    @bot.message_handler(commands=["نقاطي"])
    def my_points(message: Message):
        points = get_points(message.from_user.id, message.chat.id)
        bot.reply_to(message, f"نقاطك: {points}")

    @bot.message_handler(commands=["رتبتي"])
    def my_role(message: Message):
        role = get_role(message.from_user.id, message.chat.id)
        bot.reply_to(message, f"رتبتك: {role}")

    @bot.message_handler(commands=["معلوماتي"])
    def my_info(message: Message):
        text = get_user_info(bot, message.from_user, message.chat.id)
        bot.reply_to(message, text, parse_mode="Markdown")

    @bot.message_handler(commands=["صورتي", "صورتي_الشخصية"])
    def my_photo(message: Message):
        user_id = message.from_user.id
        photos = bot.get_user_profile_photos(user_id)
        if photos.total_count > 0:
            file_id = photos.photos[0][0].file_id
            bot.send_photo(message.chat.id, file_id, caption=f"صورة @{message.from_user.username}" if message.from_user.username else "صورتك")
        else:
            bot.reply_to(message, "❗️ لا يوجد صورة شخصية.")

    # يمكنك إضافة أوامر أخرى للأعضاء هنا بسهولة مثل: نقاط_الكل، ترتيب_التوب، الخ...
