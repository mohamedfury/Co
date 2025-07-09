import random
import string
import datetime
from telebot.types import Message, User

def random_id(length=8):
    """توليد آيدي عشوائي مكون من أرقام وحروف"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def format_time(dt=None, fmt="%Y-%m-%d %H:%M"):
    """تنسيق التاريخ والوقت لنص قابل للقراءة"""
    if not dt:
        dt = datetime.datetime.now()
    if isinstance(dt, (int, float)):
        dt = datetime.datetime.fromtimestamp(dt)
    return dt.strftime(fmt)

def time_since(dt):
    """إرجاع نص كم مضى على وقت معين (قبل 3 ساعات...)"""
    if isinstance(dt, (int, float)):
        dt = datetime.datetime.fromtimestamp(dt)
    now = datetime.datetime.now()
    diff = now - dt
    seconds = diff.total_seconds()
    if seconds < 60:
        return "الآن"
    elif seconds < 3600:
        m = int(seconds // 60)
        return f"قبل {m} دقيقة"
    elif seconds < 86400:
        h = int(seconds // 3600)
        return f"قبل {h} ساعة"
    else:
        d = int(seconds // 86400)
        return f"قبل {d} يوم"

def mention(user: User, name=None):
    """توليد منشن تليجرام بالاسم"""
    if not name:
        name = user.first_name or "مستخدم"
    return f"[{name}](tg://user?id={user.id})"

def get_username(user: User):
    """إرجاع يوزر العضو بصيغة @ أو نص بديل"""
    return f"@{user.username}" if user.username else f"`{user.id}`"

def short_id(user: User):
    """اختصار للآيدي أو اليوزر"""
    return user.username if user.username else str(user.id)

def extract_user_id(message: Message, fallback=None):
    """استخراج آيدي العضو من رسالة (reply أو mention أو نص رقم)"""
    if message.reply_to_message:
        return message.reply_to_message.from_user.id
    entities = getattr(message, "entities", []) or []
    # بحث عن منشن
    for entity in entities:
        if entity.type == "text_mention":
            return entity.user.id
    # بحث عن رقم في النص
    try:
        num = int(message.text.split()[-1])
        return num
    except Exception:
        return fallback

def get_chat_title(chat):
    """إرجاع اسم أو عنوان المجموعة/الشات"""
    return getattr(chat, 'title', None) or getattr(chat, 'first_name', 'دردشة')

def escape_markdown(text):
    """هروب رموز markdown في نص"""
    symbols = r"\_*[]()~`>#+-=|{}.!"
    for ch in symbols:
        text = text.replace(ch, f"\\{ch}")
    return text

def safe_call(func, *args, **kwargs):
    """استدعاء دالة بأمان مع تجاهل الأخطاء وإرجاع None"""
    try:
        return func(*args, **kwargs)
    except Exception:
        return None

def get_user_info_text(user: User, role=None):
    """نص مختصر لمعلومات العضو"""
    role_part = f"\n⭐️ الرتبة: {role}" if role else ""
    return (
        f"👤 الاسم: {escape_markdown(user.first_name or '')}\n"
        f"🆔 آيدي: `{user.id}`\n"
        f"🏷 اسم المستخدم: {get_username(user)}"
        f"{role_part}"
    )

# يمكنك إضافة أدوات أخرى حسب الحاجة!

# مثال استخدام:
# from utils import helpers
# text = helpers.mention(user)
# date = helpers.format_time()
