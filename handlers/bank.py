import os
import json
from telebot.types import Message

DATA = "data"
BANK_FILE = os.path.join(DATA, "bank_accounts.json")

def load_bank_data():
    if not os.path.exists(BANK_FILE):
        return {}
    with open(BANK_FILE, encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {}

def save_bank_data(data):
    with open(BANK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def register(bot):

    @bot.message_handler(commands=['انشاء_حساب'])
    def create_account(message: Message):
        user_id = str(message.from_user.id)
        bank_data = load_bank_data()
        if user_id in bank_data:
            bot.reply_to(message, "❗️ لديك حساب بنكي بالفعل.")
        else:
            bank_data[user_id] = {
                "balance": 0,
                "debt": 0,
                "last_salary": 0
            }
            save_bank_data(bank_data)
            bot.reply_to(message, "✅ تم إنشاء حسابك البنكي بنجاح.")

    @bot.message_handler(commands=['حسابي'])
    def account_info(message: Message):
        user_id = str(message.from_user.id)
        bank_data = load_bank_data()
        if user_id not in bank_data:
            bot.reply_to(message, "❗️ ليس لديك حساب بنكي، أنشئ حساب أولاً باستخدام /انشاء_حساب")
            return
        account = bank_data[user_id]
        text = (
            f"💰 رصيدك الحالي: {account.get('balance', 0)} ريال\n"
            f"💸 الدين: {account.get('debt', 0)} ريال\n"
            f"🎁 آخر راتب استلمته: {account.get('last_salary', 0)} ريال"
        )
        bot.reply_to(message, text)

    # أضف أوامر أخرى متعلقة بالبنك هنا مثل تحويل، سحب، إيداع...
