# handlers/inline.py

from telebot.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

def register(bot):
    # مثال: بحث إنلاين – يرجع نتائج عند كتابة اسم البوت في أي محادثة
    @bot.inline_handler(lambda query: True)
    def default_inline(inline_query: InlineQuery):
        results = []

        # مثال ثابت: 3 نتائج جاهزة (يمكنك ربطها ببحث أو قاعدة بيانات)
        results.append(
            InlineQueryResultArticle(
                id="1",
                title="رسالة ترحيب",
                description="أرسل رسالة ترحيب جاهزة",
                input_message_content=InputTextMessageContent("أهلاً بك في البوت الإداري! 👋"),
            )
        )
        results.append(
            InlineQueryResultArticle(
                id="2",
                title="قوانين المجموعة",
                description="أرسل قوانين المجموعة مباشرة",
                input_message_content=InputTextMessageContent("❗ قوانين المجموعة:\n1- الاحترام\n2- عدم السب\n3- عدم نشر الروابط"),
            )
        )
        results.append(
            InlineQueryResultArticle(
                id="3",
                title="معلومات البوت",
                description="أرسل معلومات عن البوت",
                input_message_content=InputTextMessageContent("🤖 هذا بوت إدارة مجموعات مع ميزات متقدمة."),
            )
        )

        # أضف نتائج ديناميكية هنا حسب الحاجة (بحث، تحويل، إلخ)

        bot.answer_inline_query(inline_query.id, results, cache_time=1)
