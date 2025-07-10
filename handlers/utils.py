from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

def register(bot):
    @bot.inline_handler(func=lambda query: True)
    def inline_query_handler(inline_query):
        try:
            results = [
                bot.types.InlineQueryResultArticle(
                    id='1',
                    title='بوت قنوات',
                    input_message_content=bot.types.InputTextMessageContent(
                        '🛰 بوت إدارة قنوات مميز 🔥'
                    ),
                    description='اضغط للإرسال',
                    thumb_url='https://example.com/thumb.jpg'
                )
            ]
            bot.answer_inline_query(inline_query.id, results)
        except Exception as e:
            print("Inline Error:", e)
