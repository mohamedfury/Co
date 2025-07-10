import os
import json

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def _full_path(filename):
    """إرجاع المسار الكامل للملف داخل مجلد data"""
    return os.path.join(DATA_DIR, filename)

def load_json(filename, default=None):
    """تحميل بيانات json من ملف، مع قيمة افتراضية في حال الخطأ"""
    fullpath = _full_path(filename)
    if not os.path.exists(fullpath):
        return default if default is not None else {}
    try:
        with open(fullpath, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else {}

def save_json(filename, data):
    """حفظ بيانات json في ملف"""
    fullpath = _full_path(filename)
    with open(fullpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_item(filename, main_key, sub_key=None, default=None):
    """جلب عنصر (أو قيمة فرعية) من ملف dict (مثل users.json أو groups.json)"""
    data = load_json(filename)
    if sub_key is not None:
        return data.get(str(main_key), {}).get(str(sub_key), default)
    return data.get(str(main_key), default)

def set_item(filename, main_key, value, sub_key=None):
    """حفظ عنصر (أو قيمة فرعية) في ملف dict"""
    data = load_json(filename)
    main_key = str(main_key)
    if sub_key is not None:
        if main_key not in data or not isinstance(data[main_key], dict):
            data[main_key] = {}
        data[main_key][str(sub_key)] = value
    else:
        data[main_key] = value
    save_json(filename, data)

def delete_item(filename, main_key, sub_key=None):
    """حذف عنصر (أو قيمة فرعية) من ملف dict"""
    data = load_json(filename)
    main_key = str(main_key)
    if sub_key is not None and main_key in data and str(sub_key) in data[main_key]:
        del data[main_key][str(sub_key)]
        # إذا أصبح القاموس الفرعي فارغاً يمكن حذفه كاملاً
        if not data[main_key]:
            del data[main_key]
    elif main_key in data:
        del data[main_key]
    save_json(filename, data)

def append_to_list(filename, item):
    """إضافة عنصر لقائمة json (مثل replies.json أو fun_lists.json)"""
    data = load_json(filename, default=[])
    if not isinstance(data, list):
        data = []
    if item not in data:
        data.append(item)
        save_json(filename, data)

def remove_from_list(filename, item):
    """حذف عنصر من قائمة json"""
    data = load_json(filename, default=[])
    if not isinstance(data, list):
        return
    if item in data:
        data.remove(item)
        save_json(filename, data)

def clear_file(filename):
    """إفراغ ملف json (dict أو list)"""
    ext = os.path.splitext(filename)[-1]
    default = [] if ext == ".list" else {}
    save_json(filename, default)

# --- أمثلة استخدام ---
# users = load_json("users.json")
# set_item("users.json", chat_id, {"messages": 5, "points": 99})
# set_item("users.json", chat_id, 10, sub_key=user_id)
# delete_item("users.json", chat_id)
# append_to_list("replies.json", "رد جديد")
# remove_from_list("replies.json", "رد جديد")
