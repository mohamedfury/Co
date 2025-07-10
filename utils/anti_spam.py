import time
import os
import json

DATA_DIR = "data"
SPAM_FILE = os.path.join(DATA_DIR, "spam_status.json")
os.makedirs(DATA_DIR, exist_ok=True)

def _load_spam():
    if not os.path.exists(SPAM_FILE):
        return {}
    try:
        with open(SPAM_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_spam(data):
    with open(SPAM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def reset_user(chat_id, user_id):
    """إعادة تعيين عداد المستخدم يدوياً (مثلاً بعد الحظر)"""
    data = _load_spam()
    chat = data.setdefault(str(chat_id), {})
    if str(user_id) in chat:
        del chat[str(user_id)]
    _save_spam(data)

def is_spam(message, max_msgs=6, interval=5, max_mentions=4, block_links=True):
    """
    فحص هل الرسالة سبام (تكرار سريع أو تفليش منشن أو روابط)
    - max_msgs: أقصى عدد رسائل بنفس الفترة (interval بالثواني)
    - max_mentions: أقصى عدد منشن بنفس الرسالة
    - block_links: تفعيل حماية الروابط
    """
    chat_id = message.chat.id
    user_id = message.from_user.id
    now = time.time()
    data = _load_spam()
    chat = data.setdefault(str(chat_id), {})
    user = chat.setdefault(str(user_id), {
        "timestamps": [],
        "last_text": "",
        "duplicates": 0
    })

    # عداد تكرار الرسائل السريعة
    user["timestamps"] = [t for t in user["timestamps"] if now - t < interval]
    user["timestamps"].append(now)
    if len(user["timestamps"]) > max_msgs:
        _save_spam(data)
        return "spam"  # سبام رسائل سريعة

    # عداد تكرار نفس الرسالة (تفليش نص متكرر)
    if message.text:
        if user["last_text"] == message.text:
            user["duplicates"] += 1
        else:
            user["duplicates"] = 1
        user["last_text"] = message.text
        if user["duplicates"] >= 4:
            _save_spam(data)
            return "duplicate"  # سبام نص متكرر

    # عداد المنشنات في الرسالة
    if hasattr(message, "entities") and message.entities:
        mentions = sum(1 for e in message.entities if e.type in ["mention", "text_mention"])
        if mentions >= max_mentions:
            _save_spam(data)
            return "mentions"  # سبام منشن

    # حماية الروابط
    if block_links and message.text:
        if "http://" in message.text or "https://" in message.text or "t.me/" in message.text:
            _save_spam(data)
            return "link"  # سبام روابط

    # حماية الملصقات (بدون إضافة timestamp ثانية)
    if hasattr(message, "sticker") and message.sticker:
        if len(user["timestamps"]) > max_msgs + 2:
            _save_spam(data)
            return "stickers"  # سبام ملصقات

    # حفظ الحالة
    _save_spam(data)
    return None  # لا يوجد سبام

def anti_spam_decorator(max_msgs=6, interval=5, max_mentions=4, block_links=True, action=None):
    """
    ديكوريتر يمكنك وضعه على أي هاندلر لمنع السبام تلقائياً
    - action: دالة تنفذ عند كشف سبام (مثلاً كتم العضو أو حذف الرسالة)
    """
    def decorator(handler):
        def wrapper(message, *args, **kwargs):
            reason = is_spam(
                message,
                max_msgs=max_msgs,
                interval=interval,
                max_mentions=max_mentions,
                block_links=block_links
            )
            if reason:
                if action:
                    return action(message, reason)
                # افتراضياً يتم تجاهل الرسالة
                return
            return handler(message, *args, **kwargs)
        return wrapper
    return decorator

# مثال عملي (ضعه في هاندلر الرسائل):
# from utils.anti_spam import anti_spam_decorator
#
# @anti_spam_decorator(action=lambda msg, reason: bot.delete_message(msg.chat.id, msg.message_id))
# def all_messages_handler(message):
#     # معالجة الرسائل العادية فقط إذا لم تكن سبام
#     pass
