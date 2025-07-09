# handlers/bank.py

import os
import json
from telebot.types import Message

DATA = "data"
BANK_FILE = os.path.join(DATA, "bank.json")

def load_balances():
    if not os.path.exists(BANK_FILE):
        return {}
    with open(BANK_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_balances(balances):
    with open(BANK_FILE, "w", encoding="utf-8") as f:
        json.dump(balances, f, ensure_ascii=False, indent=2)

def get_balance(user_id):
    balances = load_balances()
    return balances.get(str(user_id), 0)

def set_balance(user_id, amount):
    balances = load_balances()
    balances[str(user_id)] = amount
    save_balances(balances)

def add_balance(user_id, amount):
    balances = load_balances()
    balances[str(user_id)] = balances.get(str(user_id), 0) + amount
    save_balances(balances)

def deduct_balance(user_id, amount):
    balances = load_balances()
    current = balances.get(str(user_id), 0)
    balances[str(user_id)] = max(0, current - amount)
    save_balances(balances)

def register(bot):
    # عرض الرصيد
    @bot.message_handler(commands=['رصيدي'])
    def my_balance(message: Message):
        balance = get_balance(message.from_user.id)
        bot.reply_to(message, f"رصيدك الحالي: {balance} نقطة.")

    # إضافة نقاط (للأدمين فقط) بالرد
    @bot.message_handler(commands=['اضافة_نقاط'])
    def add_points(message: Message):
        if not message.reply_to_message or len(message.text.split()) < 2:
            return bot.reply_to(message, "استخدم: اضافة_نقاط 50 (بالرد على العضو)")
        try:
            amount = int(message.text.split()[1])
        except Exception:
            return bot.reply_to(message, "يرجى كتابة عدد النقاط بشكل صحيح.")
        user_id = message.reply_to_message.from_user.id
        add_balance(user_id, amount)
        bot.reply_to(message, f"تم إضافة {amount} نقطة للعضو.")

    # خصم نقاط (للأدمين فقط) بالرد
    @bot.message_handler(commands=['خصم_نقاط'])
    def deduct_points(message: Message):
        if not message.reply_to_message or len(message.text.split()) < 2:
            return bot.reply_to(message, "استخدم: خصم_نقاط 20 (بالرد على العضو)")
        try:
            amount = int(message.text.split()[1])
        except Exception:
            return bot.reply_to(message, "يرجى كتابة عدد النقاط بشكل صحيح.")
        user_id = message.reply_to_message.from_user.id
        deduct_balance(user_id, amount)
        bot.reply_to(message, f"تم خصم {amount} نقطة من العضو.")

    # تحويل نقاط (من عضو لعضو)
    @bot.message_handler(commands=['تحويل'])
    def transfer_points(message: Message):
        if not message.reply_to_message or len(message.text.split()) < 2:
            return bot.reply_to(message, "استخدم: تحويل 10 (بالرد على العضو المستلم)")
        try:
            amount = int(message.text.split()[1])
        except Exception:
            return bot.reply_to(message, "يرجى كتابة عدد النقاط بشكل صحيح.")
        from_id = message.from_user.id
        to_id = message.reply_to_message.from_user.id
        if from_id == to_id:
            return bot.reply_to(message, "لا يمكنك تحويل نقاط لنفسك.")
        if get_balance(from_id) < amount:
            return bot.reply_to(message, "رصيدك غير كافٍ للتحويل.")
        deduct_balance(from_id, amount)
        add_balance(to_id, amount)
        bot.reply_to(message, f"تم تحويل {amount} نقطة بنجاح.")

    # عرض رصيد بالرد على عضو
    @bot.message_handler(commands=['رصيد'])
    def user_balance(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على عضو لمعرفة رصيده.")
        user = message.reply_to_message.from_user
        balance = get_balance(user.id)
        bot.reply_to(message, f"رصيد {user.first_name}: {balance} نقطة.")
