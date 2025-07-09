# handlers/groups.py

import os
import json
from telebot.types import Message

DATA = "data"
SETTINGS_FILE = os.path.join(DATA, "group_settings.json")
WELCOME_FILE = os.path.join(DATA, "welcomes.json")
RULES_FILE = os.path.join(DATA, "rules.json")

# دوال مساعدة للتحميل والحفظ
def load_settings(chat_id):
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(chat_id), {})

def save_settings(chat_id, settings):
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(SETTINGS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    data[str(chat_id)] = settings
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_textfile(filename, chat_id):
    if not os.path.exists(filename):
        return ""
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(chat_id), "")

def save_textfile(filename, chat_id, text):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    data[str(chat_id)] = text
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def register(bot):

    # تفعيل/تعطيل ميزات
    @bot.message_handler(commands=['تفعيل', 'تعطيل'])
    def toggle_feature(message: Message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return bot.reply_to(message, "يرجى تحديد اسم الميزة.\nمثال: تفعيل الترحيب")
        action, feature = args[0], args[1].strip()
        features = ["الترحيب", "الرابط", "التحقق", "الالعاب", "التحشيش", "اطردني"]
        if feature not in features:
            return bot.reply_to(message, "الميزة غير معروفة.")
        settings = load_settings(message.chat.id)
        settings[feature] = (action == "تفعيل")
        save_settings(message.chat.id, settings)
        status = "تم تفعيل" if action == "تفعيل" else "تم تعطيل"
        bot.reply_to(message, f"{status} {feature}.")

    # قفل/فتح ميزات
    @bot.message_handler(commands=['قفل', 'فتح'])
    def lock_unlock_feature(message: Message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return bot.reply_to(message, "يرجى تحديد ما تريد قفله أو فتحه.\nمثال: قفل الصور")
        action, feature = args[0], args[1].strip()
        lockables = ["الصور", "الروابط", "الفيديو", "الصوت", "الملفات", "المتحركة", "الملصقات", "الجهات", "التعديل"]
        if feature not in lockables:
            return bot.reply_to(message, "لا يمكن قفل/فتح هذا العنصر.")
        settings = load_settings(message.chat.id)
        settings[f"قفل_{feature}"] = (action == "قفل")
        save_settings(message.chat.id, settings)
        status = "تم قفل" if action == "قفل" else "تم فتح"
        bot.reply_to(message, f"{status} {feature}.")

    # عرض الاعدادات
    @bot.message_handler(commands=['الاعدادات'])
    def show_settings(message: Message):
        settings = load_settings(message.chat.id)
        if not settings:
            return bot.reply_to(message, "لا توجد إعدادات محفوظة لهذه المجموعة.")
        txt = "⌔︙إعدادات المجموعة:\n"
        for k, v in settings.items():
            emoji = "✅" if v else "✖️"
            txt += f"• {k} : {emoji}\n"
        bot.reply_to(message, txt)

    # تحديد الترحيب
    @bot.message_handler(commands=['ضع_ترحيب'])
    def set_welcome(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "أرسل نص الترحيب بالرد على هذه الرسالة.")
        text = message.reply_to_message.text or " "
        save_textfile(WELCOME_FILE, message.chat.id, text)
        bot.reply_to(message, "تم تغيير رسالة الترحيب.")

    # عرض الترحيب
    @bot.message_handler(commands=['الترحيب'])
    def show_welcome(message: Message):
        text = load_textfile(WELCOME_FILE, message.chat.id)
        if not text:
            return bot.reply_to(message, "لا توجد رسالة ترحيب محددة.")
        bot.reply_to(message, text)

    # وضع القوانين
    @bot.message_handler(commands=['ضع_القوانين'])
    def set_rules(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "أرسل نص القوانين بالرد على هذه الرسالة.")
        text = message.reply_to_message.text or " "
        save_textfile(RULES_FILE, message.chat.id, text)
        bot.reply_to(message, "تم حفظ القوانين.")

    # عرض القوانين
    @bot.message_handler(commands=['القوانين'])
    def show_rules(message: Message):
        text = load_textfile(RULES_FILE, message.chat.id)
        if not text:
            return bot.reply_to(message, "لا توجد قوانين محددة.")
        bot.reply_to(message, text)

    # معلومات المجموعة
    @bot.message_handler(commands=['المجموعه'])
    def group_info(message: Message):
        chat = message.chat
        info = f"""⌔︙معلومات المجموعة:
- الاسم: {chat.title}
- المعرف: {chat.username or 'لا يوجد'}
- ID: {chat.id}
- عدد الأعضاء: {bot.get_chat_members_count(chat.id)}
"""
        bot.reply_to(message, info)

    # عرض الرابط
    @bot.message_handler(commands=['الرابط'])
    def group_link(message.reply_to(message, f"رابط المجموعة:\n{link}")
        except Exception:
            bot.reply_to(message, "لا يمكن جلب رابط المجموعة (تأكد أن البوت أدمن).")
