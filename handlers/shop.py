# handlers/shop.py

import os
import json
from telebot.types import Message

DATA = "data"
PRODUCTS_FILE = os.path.join(DATA, "shop_products.json")
ORDERS_FILE = os.path.join(DATA, "shop_orders.json")

def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

def register(bot):
    # إضافة منتج (بالرد على نص المنتج: اسم - السعر - الوصف)
    @bot.message_handler(commands=['اضافة_منتج'])
    def add_product(message: Message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return bot.reply_to(message, "رد على رسالة تحتوي على: اسم المنتج - السعر - الوصف")
        try:
            name, price, desc = [x.strip() for x in message.reply_to_message.text.split('-', 2)]
        except Exception:
            return bot.reply_to(message, "الصيغة غير صحيحة. مثال: منتج جديد - 1000 - وصف قصير")
        products = load_products()
        products.append({"name": name, "price": price, "desc": desc})
        save_products(products)
        bot.reply_to(message, f"تمت إضافة المنتج: {name}")

    # حذف منتج (بالرد على اسم المنتج)
    @bot.message_handler(commands=['حذف_منتج'])
    def del_product(message: Message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return bot.reply_to(message, "رد على اسم المنتج لحذفه")
        name = message.reply_to_message.text.strip()
        products = load_products()
        filtered = [p for p in products if p["name"] != name]
        if len(filtered) == len(products):
            return bot.reply_to(message, "المنتج غير موجود.")
        save_products(filtered)
        bot.reply_to(message, f"تم حذف المنتج: {name}")

    # عرض المنتجات
    @bot.message_handler(commands=['المنتجات'])
    def show_products(message: Message):
        products = load_products()
        if not products:
            return bot.reply_to(message, "لا توجد منتجات حالياً.")
        text = "🛒 قائمة المنتجات:\n"
        for idx, p in enumerate(products, 1):
            text += f"{idx}. {p['name']} - {p['price']} : {p['desc']}\n"
        bot.reply_to(message, text)

    # شراء منتج (بالرد على اسم المنتج)
    @bot.message_handler(commands=['شراء'])
    def buy_product(message: Message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return bot.reply_to(message, "رد على اسم المنتج الذي تريد شراءه")
        name = message.reply_to_message.text.strip()
        products = load_products()
        product = next((p for p in products if p["name"] == name), None)
        if not product:
            return bot.reply_to(message, "المنتج غير موجود.")
        orders = load_orders()
        orders.append({"user_id": message.from_user.id, "username": message.from_user.username, "product": name})
        save_orders(orders)
        bot.reply_to(message, f"تم تسجيل طلبك لشراء المنتج: {name}\nسيتم التواصل معك قريباً.")

    # عرض الطلبات (للأدمين فقط)
    @bot.message_handler(commands=['الطلبات'])
    def show_orders(message: Message):
        # يمكنك تعديل شرط الصلاحية هنا
        if not message.from_user.id in [123456789]:  # عدل هذا الـ ID إلى آي دي الأدمن
            return bot.reply_to(message, "هذه الميزة للأدمن فقط.")
        orders = load_orders()
        if not orders:
            return bot.reply_to(message, "لا توجد طلبات شراء بعد.")
        text = "📦 الطلبات:\n"
        for idx, o in enumerate(orders, 1):
            text += f"{idx}. المستخدم: @{o['username'] or o['user_id']} - المنتج: {o['product']}\n"
        bot.reply_to(message, text)
