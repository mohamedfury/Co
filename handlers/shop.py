import json
import os
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

DATA = "data"
SHOP_FILE = os.path.join(DATA, "shop_items.json")

def load_shop_items():
    if not os.path.exists(SHOP_FILE):
        return {}
    with open(SHOP_FILE, encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {}

def save_shop_items(items):
    with open(SHOP_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def register(bot):

    @bot.message_handler(commands=['متجر'])
    def show_shop(message: Message):
        items = load_shop_items()
        if not items:
            bot.reply_to(message, "🚫 لا يوجد عناصر في المتجر حالياً.")
            return
        text = "🛒 قائمة العناصر في المتجر:\n\n"
        for item_id, item in items.items():
            text += f"• {item['name']} - السعر: {item['price']} نقاط\n"
        bot.reply_to(message, text)

    @bot.message_handler(commands=['اضف_عنصر'])
    def add_item(message: Message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return bot.reply_to(message, "❗️ الرجاء الرد على رسالة تحتوي على اسم العنصر.")
        name = message.reply_to_message.text.strip()
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return bot.reply_to(message, "❗️ الرجاء تحديد سعر العنصر.\nمثال: اضف_عنصر 100")
        try:
            price = int(args[1])
        except ValueError:
            return bot.reply_to(message, "❗️ السعر يجب أن يكون رقماً صحيحاً.")
        items = load_shop_items()
        new_id = str(max([int(k) for k in items.keys()] + [0]) + 1)
        items[new_id] = {"name": name, "price": price}
        save_shop_items(items)
        bot.reply_to(message, f"✅ تم إضافة العنصر '{name}' بسعر {price} نقاط.")

    @bot.message_handler(commands=['مسح_عنصر'])
    def delete_item(message: Message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return bot.reply_to(message, "❗️ الرجاء تحديد رقم العنصر لمسحه.\nمثال: مسح_عنصر 2")
        item_id = args[1].strip()
        items = load_shop_items()
        if item_id not in items:
            return bot.reply_to(message, "❗️ هذا العنصر غير موجود.")
        name = items[item_id]['name']
        del items[item_id]
        save_shop_items(items)
        bot.reply_to(message, f"✅ تم مسح العنصر '{name}'.")

    # يمكنك إضافة المزيد من أوامر المتجر مثل الشراء، العرض التفصيلي، الخ...
