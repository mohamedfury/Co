# handlers/fun.py

import random
from telebot.types import Message

JOKES = [
    "واحد ذهب للبقالة قالهم عندكم عيش؟ قالوا لا.. قال طيب عندكم موت؟ 😂",
    "مرة واحد ذهب للدكتور قال له: عندي مشكلة أنسى كثير! قال له الدكتور: من متى؟ قال: من متى إيش؟",
    "في واحد ذهب للبقالة قالهم: عندكم سكر؟ قالوا: عندنا بس لا تزعل نفسك، الحياة حلوة!",
    "مرة واحد ذهب يصيد سمك، رجع صيدليه! 🐟💊",
    "في واحد ذهب يشتغل حارس ليلي، نام في الدوام وصار ظل! 🌚"
]

LOVE_RESPONSES = [
    "نسبة حبك هي: {}% 💖",
    "تحبك بنسبة: {}% 😍",
    "حبك في القلب: {}% 💘"
]

def register(bot):

    @bot.message_handler(commands=['نكتة', 'نكت'])
    def joke(message: Message):
        bot.reply_to(message, random.choice(JOKES))

    @bot.message_handler(commands=['حب'])
    def love_meter(message: Message):
        percent = random.randint(1, 100)
        text = random.choice(LOVE_RESPONSES).format(percent)
        bot.reply_to(message, text)

    @bot.message_handler(commands=['قرعة'])
    def lottery(message: Message):
        items = message.text.split()[1:]
        if not items:
            return bot.reply_to(message, "اكتب أسماء الأشخاص بعد الأمر: قرعة أحمد علي سارة ...")
        winner = random.choice(items)
        bot.reply_to(message, f"الفائز بالقرعة هو: {winner} 🏆")

    @bot.message_handler(commands=['زواج'])
    def marry(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على رسالة العضو الذي تريد الزواج منه 😅")
        user1 = message.from_user.first_name
        user2 = message.reply_to_message.from_user.first_name
        percent = random.randint(30, 100)
        bot.reply_to(message, f"مبارك! {user1} و {user2} نسبة التوافق بينكم {percent}% 👩‍❤️‍👨")

    @bot.message_handler(commands=['تحدي'])
    def challenge(message: Message):
        challenges = [
            "ارسل آخر صورة في أستوديوك 📸",
            "اكتب سر لم يعرفه عنك أحد من قبل!",
            "ارسل تسجيل صوتي وأنت تغني أغنية تحبها 🎤",
            "ارسل إيموجي يعبر عن مزاجك الآن 😁",
            "اكتب اسم أول حب في حياتك ❤️"
        ]
        bot.reply_to(message, random.choice(challenges))

    @bot.message_handler(commands=['حزر_فزر'])
    def guess_game(message: Message):
        riddles = [
            ("شيء كلما أخذت منه كبر؟", "الحفرة"),
            ("له أسنان ولا يعض، ما هو؟", "المشط"),
            ("يمشي بلا رجلين ولا يدخل إلا بالأذنين، ما هو؟", "الصوت"),
        ]
        riddle = random.choice(riddles)
        bot.reply_to(message, f"حزر فزر: {riddle[0]}\n(الإجابة بعد دقيقة!)")

    # أضف أي لعبة أو فعالية ترفيهية أخرى هنا
