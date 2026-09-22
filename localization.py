from datetime import date, datetime


STATUS_LABELS = {
    "pending": "รอรับเรื่อง",
    "accepted": "รับเรื่องแล้ว",
    "in_progress": "กำลังดำเนินการ",
    "completed": "ซ่อมเสร็จแล้ว",
}

URGENCY_LABELS = {
    "low": "ต่ำ",
    "medium": "ปานกลาง",
    "high": "สูง",
}

PROBLEM_TYPE_LABELS = {
    "electrical": "ระบบไฟฟ้า",
    "furniture": "เฟอร์นิเจอร์",
    "computer": "คอมพิวเตอร์",
    "aircon": "เครื่องปรับอากาศ",
    "other": "อื่น ๆ",
}

ROLE_LABELS = {
    "admin": "ผู้ดูแลระบบ",
    "teacher": "ครู / บุคลากร",
    "technician": "เจ้าหน้าที่ซ่อม",
}

IMAGE_TYPE_LABELS = {
    "before": "รูปก่อนซ่อม",
    "after": "รูปหลังซ่อม",
}


def _value(value):
    return getattr(value, "value", value)


def status_label(value) -> str:
    raw = _value(value)
    return STATUS_LABELS.get(raw, raw or "—")


def urgency_label(value) -> str:
    raw = _value(value)
    return URGENCY_LABELS.get(raw, raw or "—")


def problem_type_label(value) -> str:
    raw = _value(value)
    return PROBLEM_TYPE_LABELS.get(raw, raw or "—")


def role_label(value) -> str:
    raw = _value(value)
    return ROLE_LABELS.get(raw, raw or "—")


def image_type_label(value) -> str:
    raw = _value(value)
    return IMAGE_TYPE_LABELS.get(raw, raw or "—")


def thai_date(value: date | datetime | None, include_time: bool = False) -> str:
    if not value:
        return "—"
    pattern = "%d/%m/%Y %H:%M" if include_time and isinstance(value, datetime) else "%d/%m/%Y"
    return value.strftime(pattern)

