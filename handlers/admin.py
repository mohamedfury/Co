# handlers/admin.py

import os
import json
from telebot.types import Message

DATA = "data"
FILES = {
    "vips": os.path.join(DATA, "vips.json"),
    "owners": os.path.join(DATA, "owners.json"),
    "bans": os.path.join(DATA, "bans.json"),
    "mutes": os.path.join(DATA, "mutes.json"),
    "restricts": os.path.join(DATA, "restricts.json"),
    "blocks": os.path.join(DATA, "blocks.json"),
}

def load_list(filename, chat_id):
    if not os.path.exists(filename):
        return []
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(chat_id), [])

def save_list(filename, chat_id, items):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    data[str(chat_id)] = items
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_to_list(filename, chat_id, user_id):
    items = load_list(filename, chat_id)
    if user_id not in items:
        items.append(user_id)
        save_list(filename, chat_id, items)

def remove_from_list(filename, chat_id, user_id):
    items = load_list(filename, chat_id)
    if user_id in items:
        items.remove(user_id)
        save_list(filename, chat_id, items)

def clear_list(filename, chat_id):
    save_list(filename, chat_id, [])

def list_to_text(items, bot, chat_id):
    lines = []
    for uid in items:
        try:
            user = bot.get_chat_member(chat_id, uid).user
            name = user.first_name
            lines.append(f"• [{name}](tg://user?id={uid})")
        except Exception:
            lines.append(f"• {uid}")
    return "\n".join(lines) if lines else "لا توجد عناصر بعد."

def register(bot):
    # رفع مميز
    @bot.message_handler(commands=['رفع_مميز'])
    def add_vip(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لرفعه مميز.")
        user_id = message.reply_to_message.from_user.id
        add_to_list(FILES["vips"], message.chat.id, user_id)
        bot.reply_to(message, "تم رفع العضو مميز ✅")

    # تنزيل مميز
    @bot.message_handler(commands=['تنزيل_مميز'])
    def remove_vip(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لتنزيله من المميزين.")
        user_id = message.reply_to_message.from_user.id
        remove_from_list(FILES["vips"], message.chat.id, user_id)
        bot.reply_to(message, "تم تنزيل العضو من قائمة المميزين ✅")

    # قائمة المميزين
    @bot.message_handler(commands=['المميزين'])
    def vip_list(message: Message):
        vips = load_list(FILES["vips"], message.chat.id)
        text = "قائمة المميزين:\n" + list_to_text(vips, bot, message.chat.id)
        bot.reply_to(message, text, parse_mode="Markdown")

    # مسح المميزين
    @bot.message_handler(commands=['مسح_المميزين'])
    def clear_vips(message: Message):
        clear_list(FILES["vips"], message.chat.id)
        bot.reply_to(message, "تم مسح جميع المميزين.")

    # رفع مالك
    @bot.message_handler(commands=['رفع_المالك'])
    def add_owner(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لرفعه مالك.")
        user_id = message.reply_to_message.from_user.id
        add_to_list(FILES["owners"], message.chat.id, user_id)
        bot.reply_to(message, "تم رفع العضو مالك ✅")

    # تاك للكل (تنبيه: تنفيذ جماعي قد يسبب حظر البوت من تليجرام)
    @bot.message_handler(commands=['تاك'])
    def tag_all(message: Message):
        members = []  # يجب جلب قائمة الأعضاء من قاعدة بياناتك أو من API تليجرام بحذر
        text = ""
        for uid in members:
            text += f"[{uid}](tg://user?id={uid}) "
        bot.send_message(message.chat.id, text or "لا يوجد أعضاء يمكن عمل تاك لهم.", parse_mode="Markdown")

    # منع عضو
    @bot.message_handler(commands=['منع'])
    def block_user(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لمنعه.")
        user_id =.reply_to(message, "تم منع العضو.")

    # الغاء منع
    @bot.message_handler(commands=['الغاء_منع'])
    def unblock_user(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لالغاء المنع.")
        user_id = message.reply_to_message.from_user.id
        remove_from_list(FILES["blocks"], message.chat.id, user_id)
        bot.reply_to(message, "تم الغاء منع العضو.")

    # حظر
    @bot.message_handler(commands=['حظر'])
    def ban_user(message: Message_id)
       _to(message, "تم حظر العضو 🚫")

    # الغاء حظر
    @bot.message_handler(commands=['الغاء_حظر'])
    def unban_user(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لالغاء الحظر.")
        user_id = message.reply_to_message.from_user.id
        bot.unban_chat_member(message.chat.id, user_id)
        remove_from_list(FILES["bans"], message.chat.id, user_id)
        bot.reply_to(message, "تم الغاء حظر العضو.")

    # طرد
    @.reply_to(message, "تم طرد العضو 👋")

    # تثبيت
    @bot.message_handler(commands=['تثبيت'])
    def pin_message(message: Message):
        if message.reply_to_message:
            bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
            bot.reply_to(message, "تم تثبيت الرسالة.")

    # الغاء تثبيت
    @bot.message_handler(commands=['الغاء_تثبيت'])
    def unpin_message(message: Message):
        bot.unpin_chat_message(message.chat.id)
        bot.reply_to(message, "تم الغاء تثبيت الرسالة.")

    # كتم
    @bot.message_handler(commands=['كتم'])
    def mute_user(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لكتمه.")
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=False)
        add_to_list(FILES["mutes"], message.chat.id, user_id)
        bot.reply_to(message, "تم كتم العضو.")

    # الغاء كتم
    @bot.message_handler(commands=['الغاء_كتم'])
    def unmute_user(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لالغاء الكتم.")
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=True)
        remove_from_list(FILES[".chat.id, user_id)
        bot.reply_to(message, "تم الغاء كتم العضو.")

    # تقييد
    @bot.message_handler(commands=['تقييد'])
    def restrict_user(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لتقييده.")
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=False, can_send_media_messages=False, can_send_polls=False, can_add_web_page_previews=False)
        add_to_list(FILES["restricts"],.id)
        bot.reply_to(message, text, parse_mode="Markdown")
