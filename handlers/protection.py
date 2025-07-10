# handlers/protection.py

import os
import json
import re
from telebot.types import Message

DATA = "data"
PROTECTION_FILE = os.path.join(DATA, "protection_settings.json")
BLOCKED_WORDS_FILE = os.path.join(DATA, "blocked_words.json")

def load_settings(chat_id):
    if not os.path.exists(PROTECTION_FILE):  # صححت if الشرط هنا
        return {}
    with open(PROTECTION_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(chat_id), {})

def save_settings(chat_id, settings):
    if not os.path.exists(PROTECTION_FILE):
        with open(PROTECTION_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(PROTECTION_FILE, encoding="utf-8") as f:
        data = json.load(f)
    data[str(chat_id)] = settings
    with open(PROTECTION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_blocked_words(chat_id):
    if not os.path.exists(BLOCKED_WORDS_FILE):
        return []
    with open(BLOCKED_WORDS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(chat_id), [])

def save_blocked_words(chat_id, words):
    if not os.path.exists(BLOCKED_WORDS_FILE):
        with open(BLOCKED_WORDS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(BLOCKED_WORDS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    data[str(chat_id)] = words
    with open(BLOCKED_WORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def register(bot):

    # تفعيل/تعطيل الحماية من الروابط
    @bot.message_handler(commands=['تفعيل_حماية_الروابط', 'تعطيل_حماية_الروابط'])
    def toggle_link_protection(message: Message):
        settings = load_settings(message.chat.id)
        if 'تفعيل' in message.text:
            settings['links'] = True
            status = "تم تفعيل الحماية من الروابط."
        else:
            settings['links'] = False
            status = "تم تعطيل الحماية من الروابط."
        save_settings(message.chat.id, settings)
        bot.reply_to(message, status)

    # تفعيل/تعطيل الحماية من التوجيه
    @bot.message_handler(commands=['تفعيل_حماية_التوجيه', 'تعطيل_حماية_التوجيه'])
    def toggle_forward_protection(message: Message):
        settings = load_settings(message.chat.id)
        if 'تفعيل' in message.text:
            settings['forward'] = True
            status = "تم تفعيل الحماية من التوجيه."
        else:
            settings['forward'] = False
            status = "تم تعطيل الحماية من التوجيه."
        save_settings(message.chat.id, settings)
        bot.reply_to(message, status)

    # تفعيل/تعطيل مكافحة التكرار (Flood)
    @bot.message_handler(commands=['تفعيل_مكافحة_التكرار', 'تعطيل_مكافحة_التكرار'])
    def toggle_flood_protection(message: Message):
        settings = load_settings(message.chat.id)
        if 'تفعيل' in message.text:
            settings['flood'] = True
            status = "تم تفعيل مكافحة التكرار."
        else:
            settings['flood'] = False  # صححت هنا السطر الغير مكتمل
            status = "تم تعطيل مكافحة التكرار."
        save_settings(message.chat.id, settings)
        bot.reply_to(message, status)

    # تفعيل/تعطيل مكافحة السبام
    @bot.message_handler(commands=['تفعيل_مكافحة_السبام', 'تعطيل_مكافحة_السبام'])
    def toggle_spam_protection(message: Message):
        settings = load_settings(message.chat.id)
        if 'تفعيل' in message.text:
            settings['spam'] = True
            status = "تم تفعيل مكافحة السبام."
        else:
            settings['spam'] = False
            status = "تم تعطيل مكافحة السبام."
        save_settings(message.chat.id, settings)
        bot.reply_to(message, status)

    # منع كلمة
    @bot.message_handler(commands=['منع_كلمة'])
    def block_word(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على كلمة تريد منعها.")
        word = message.reply_to_message.text.strip()
        words = load_blocked_words(message.chat.id)
        if word not in words:
            words.append(word)
            save_blocked_words(message.chat.id, words)
        bot.reply_to(message, f"تم منع الكلمة: {word}")

    # الغاء منع كلمة
    @bot.message_handler(commands=['الغاء_منع_كلمة'])
    def unblock_word(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على كلمة تريد الغاء منعها.")
        word = message.reply_to_message.text.strip()
        words = load_blocked_words(message.chat.id)
        if word in words:
            words.remove(word)
            save_blocked_words(message.chat.id, words)
        bot.reply_to(message, f"تم الغاء منع الكلمة: {word}")

    # عرض الكلمات الممنوعة
    @bot.message_handler(commands=['قائمة_الكلمات_الممنوعة'])
    def list_blocked_words(message: Message):
        words = load_blocked_words(message.chat.id)
        if words:
            text = "الكلمات الممنوعة:\n" + "\n".join(f"• {w}" for w in words)
        else:
            text = "لا توجد كلمات ممنوعة."
        bot.reply_to(message, text)

    # حماية تلقائية: حذف الروابط/التوجيه/الكلمات الممنوعة/التكرار/السبام
    @bot.message_handler(func=lambda m: True, content_types=['text', 'forwarded', 'photo', 'video', 'audio', 'document', 'sticker'])
    def auto_protection(message: Message):
        settings = load_settings(message.chat.id)
        # حذف الروابط
        if settings.get('links') and message.text and re.search(r"(https?://|t\.me/|telegram\.me/)", message.text):
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except Exception:
                pass
            return
        # حذف التوجيه
        if settings.get('forward') and getattr(message, 'forward_from', None):
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except Exception:
                pass
            return
        # حذف الكلمات الممنوعة
        words = load_blocked_words(message.chat.id)
        if words and message.text:
            for w in words:
                if w in message.text:
                    try:
                        bot.delete_message(message.chat.id, message.message_id)
                    except Exception:
                        pass
                    return
        # (يمكنك إضافة منطق التكرار والسبام هنا حسب الحاجة)
