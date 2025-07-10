import random
from telebot.types import Message

def register(bot):

    @bot.message_handler(commands=['نسبة_حب'])
    def love_percentage(message: Message):
        percentage = random.randint(0, 100)
        bot.reply_to(message, f"💖 نسبة الحب عندك هي: {percentage}%")

    @bot.message_handler(commands=['نسبة_كره'])
    def hate_percentage(message: Message):
        percentage = random.randint(0, 100)
        bot.reply_to(message, f"💔 نسبة الكره عندك هي: {percentage}%")

    @bot.message_handler(commands=['نسبة_ذكاء'])
    def intelligence_percentage(message: Message):
        percentage = random.randint(0, 100)
        bot.reply_to(message, f"🧠 نسبة الذكاء عندك هي: {percentage}%")

    @bot.message_handler(commands=['نسبة_غباء'])
    def stupidity_percentage(message: Message):
        percentage = random.randint(0, 100)
        bot.reply_to(message, f"🤪 نسبة الغباء عندك هي: {percentage}%")

    @bot.message_handler(commands=['شنو_رايك'])
    def what_do_you_think(message: Message):
        responses = [
            "👌 ممتاز!",
            "🙂 تمام، شكراً لسؤالك.",
            "🤔 محتاج أفكر أكثر.",
            "😐 عادي.",
            "🙄 ما أدري."
        ]
        bot.reply_to(message, random.choice(responses))

    @bot.message_handler(commands=['انطي_هدية'])
    def give_gift(message: Message):
        gifts = [
            "🎁 هدية لك!",
            "🎉 مفاجأة سعيدة!",
            "🌟 أفضل الهدايا لك!",
            "💝 مع تحياتي."
        ]
        bot.reply_to(message, random.choice(gifts))

    @bot.message_handler(commands=['بوسه'])
    def kiss(message: Message):
        kisses = [
            "😘 بوسة حارة!",
            "😚 بوسة من القلب.",
            "😍 بوسة غرامية!"
        ]
        bot.reply_to(message, random.choice(kisses))

    @bot.message_handler(commands=['رزله'])
    def insult(message: Message):
        insults = [
            "😜 يا نجم الطلع!",
            "😏 شوية هدوء يا صاحبي.",
            "😂 حلوة المزحة!"
        ]
        bot.reply_to(message, random.choice(insults))

    # ممكن تضيف أوامر ترفيهية أخرى هنا
