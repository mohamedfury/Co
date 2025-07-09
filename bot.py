import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN

# استيراد نصوص الأوامر من ملف خارجي
import messages

# استيراد جميع الملفات (handlers) التي فيها register(bot)
from handlers import (
    admin, groups, protection, managers, owners, creators, members,
    fun, bank, shop, welcome, inline, broadcast, stats, utils as handlers_utils
)

bot = telebot.TeleBot(TOKEN)

# تسجيل جميع ملفات الأوامر
handlers_list = [
    admin, groups, protection, managers, owners, creators, members,
    fun, bank, shop, welcome, inline, broadcast, stats, handlers_utils
]
for handler in handlers_list:
    if hasattr(handler, "register"):
        handler.register(bot)

# ----------- القائمة الرئيسية -----------
def send_main_menu(chat_id, message_id=None):
    text = messages.WELCOME_MSG
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("اوامر الادمن", callback_data="cmd_admin"),
        InlineKeyboardButton("اوامر المدير", callback_data="cmd_manager"),
        InlineKeyboardButton("اوامر المنشئين", callback_data="cmd_creator"),
        InlineKeyboardButton("اوامر المالكين", callback_data="cmd_owner"),
        InlineKeyboardButton("اوامر التشليه", callback_data="cmd_fun"),
        InlineKeyboardButton("اوامر البنك", callback_data="cmd_bank"),
        InlineKeyboardButton("اوامر المطور", callback_data="cmd_dev")
    )
    if message_id:
        bot.edit_message_text(text, chat_id, message_id, reply_markup=markup)
    else:
        bot.send_message(chat_id, text, reply_markup=markup)

# ----------- عرض القائمة عند كلمة "اوامر" أو "مساعدة" -----------
@bot.message_handler(func=lambda m: m.text and ("اوامر" in m.text or "مساعدة" in m.text))
def show_menu(message):
    send_main_menu(message.chat.id)

# ----------- رسالة الترحيب عند /start -----------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_main_menu(message.chat.id)

# ----------- عرض أوامر كل قسم مع زر رجوع -----------
@bot.callback_query_handler(func=lambda call: call.data.startswith("cmd_"))
def send_section_commands(call):
    section = call.data
    if section == "cmd_admin":
        msg = messages.ADMIN_COMMANDS
    elif section == "cmd_manager":
        msg = messages.MANAGER_COMMANDS
    elif section == "cmd_creator":
        msg = messages.CREATOR_COMMANDS
    elif section == "cmd_owner":
        msg = messages.OWNER_COMMANDS
    elif section == "cmd_fun":
        msg = messages.FUN_COMMANDS
    elif section == "cmd_bank":
        msg = messages.BANK_COMMANDS
    elif section == "cmd_dev":
        msg = messages.DEV_COMMANDS
    else:
        msg = "❓ عذراً، القسم غير معروف."
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬅️ رجوع للقائمة الرئيسية", callback_data="cmd_back"))
    bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup)
    bot.answer_callback_query(call.id)

# ----------- زر الرجوع للقائمة الرئيسية -----------
@bot.callback_query_handler(func=lambda call: call.data == "cmd_back")
def back_to_main_menu(call):
    send_main_menu(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)

# ----------- تشغيل البوت -----------
if __name__ == "__main__":
    print("🤖 Bot Started...")
    bot.infinity_polling()
