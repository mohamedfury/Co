# handlers/owners.py

import os
import json
from telebot.types import Message

DATA = "data"
OWNERS_FILE = os.path.join(DATA, "owners.json")

def load_owners(chat_id):
    if not os.path.exists(OWNERS_FILE):
        return []
    with open(OWNERS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(chat_id), [])

def save_owners(chat_id, owners):
    if not os.path.exists(OWNERS_FILE):
        with open(OWNERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(OWNERS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    data[str(chat_id)] = owners
    with open(OWNERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_owner(chat_id, user_id):
    owners = load_owners(chat_id)
    if user_id not in owners:
        owners.append(user_id)
        save_owners(chat_id, owners)

def remove_owner(chat_id, user_id):
    owners = load_owners(chat_id)
    if user_id in owners:
        owners.remove(user_id)
        save_owners(chat_id, owners)

def clear_owners(chat_id):
    save_owners(chat_id, [])

def list_to_text(items, bot, chat_id):
    lines = []
    for uid in items:
        try:
            user = bot.get_chat_member(chat_id, uid).user
            lines.append(f"• [{user.first_name}](tg://user?id={uid})")
        except Exception:
            lines.append(f"• {uid}")
    return "\n".join(lines) if lines else "لا يوجد مالكين حالياً."

def register(bot):
    @bot.message_handler(commands=['رفع_مالك'])
    def promote_owner(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لرفعه مالك.")
        user_id = message.reply_to_message.from_user.id
        add_owner(message.chat.id, user_id)
        bot.reply_to(message, "تم رفع العضو مالك ✅")

    @bot.message_handler(commands=['تنزيل_مالك'])
    def demote_owner(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لتنزيله من المالكين.")
        user_id = message.reply_to_message.from_user.id
        remove_owner(message.chat.id, user_id)
        bot.reply_to(message, "تم تنزيل العضو من المالكين ✅")

    @bot.message_handler(commands=['المالكين'])
    def show_owners(message: Message):
        owners = load_owners(message.chat.id)
        text = "قائمة المالكين:\n" + list_to_text(owners, bot, message.chat.id)
        bot.reply_to(message, text, parse_mode="Markdown")

    @bot.message_handler(commands=['مسح_المالكين'])
    def clear_all_owners(message: Message):
        clear_owners(message.chat.id)
        bot.reply_to(message, "تم مسح جميع المالكين من المجموعة.")
