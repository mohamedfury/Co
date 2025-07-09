# handlers/stats.py

import os
import json
from telebot.types import Message

DATA = "data"
FILES = {
    "vips": os.path.join(DATA, "vips.json"),
    "managers": os.path.join(DATA, "managers.json"),
    "bans": os.path.join(DATA, "bans.json"),
    "mutes": os.path.join(DATA, "mutes.json"),
    "restricts": os.path.join(DATA, "restricts.json"),
    "blocks": os.path.join(DATA, "blocks.json"),
    "owners": os.path.join(DATA, "owners.json"),
}

def load_list(filename, chat_id):
    if not os.path.exists(filename):
        return []
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(chat_id), [])

def register(bot):
    @bot.message_handler(commands=['الاحصائيات', 'احصائيات'])
    def group_stats(message: Message):
        chat_id = message.chat.id
        stats = {}

        # عدد الأعضاء
        try:
            stats["عدد الأعضاء"] = bot.get_chat_members_count(chat_id)
        except Exception:
            stats["عدد الأعضاء"] = "؟"

        # باقي الإحصائيات من ملفات التخزين
        stats["المميزين"] = len(load_list(FILES["vips"], chat_id))
        stats["المدراء"] = len(load_list(FILES["managers"], chat_id))
        stats["المحظورين"] = len(load_list(FILES["bans"], chat_id))
        stats["المكتومين"] = len(load_list(FILES["mutes"], chat_id))
        stats["المقيدين"] = len(load_list(FILES["restricts"], chat_id))
        stats["الممنوعين"] = len(load_list(FILES["blocks"], chat_id))
        stats["المالكين"] = len(load_list(FILES["owners"], chat_id))

        # إذا عندك نظام عداد رسائل يومي/شهري أضف الكود هنا

        # بناء الرسالة
        msg = f"""⌔︙إحصائيات المجموعة:
        
👤︙عدد الأعضاء: {stats["عدد الأعضاء"]}
⭐︙عدد المميزين: {stats["المميزين"]}
🛡︙عدد المدراء: {stats["المدراء"]}
🚫︙عدد المحظورين: {stats["المحظورين"]}
🔇︙عدد المكتومين: {stats["المكتومين"]}
⛔︙عدد المقيدين: {stats["المقيدين"]}
❌︙عدد الممنوعين: {stats["الممنوعين"]}
👑︙عدد المالكين: {stats["المالكين"]}
"""
        bot.reply_to(message, msg)
