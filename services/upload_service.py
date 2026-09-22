import uuid
from pathlib import Path

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from enums import ImageType
from extensions import db
from models import RepairImage, RepairRequest


class UploadService:
    MIME_TYPES = {"image/jpeg", "image/png", "image/gif"}
    @staticmethod
    def _detected_type(header: bytes) -> str | None:
        if header.startswith(b"\xff\xd8\xff"):
            return "jpg"
        if header.startswith(b"\x89PNG\r\n\x1a\n"):
            return "png"
        if header.startswith((b"GIF87a", b"GIF89a")):
            return "gif"
        return None

    @classmethod
    def validate(cls, file: FileStorage) -> str:
        original = secure_filename(file.filename or "")
        if not original or "." not in original:
            raise ValueError("ชื่อไฟล์รูปภาพไม่ถูกต้อง")
        extension = original.rsplit(".", 1)[1].lower()
        if extension not in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            raise ValueError("รองรับเฉพาะรูปภาพ JPG, PNG และ GIF")
        if file.mimetype not in cls.MIME_TYPES:
            raise ValueError("ไฟล์ที่อัปโหลดไม่ใช่รูปภาพที่รองรับ")
        header = file.stream.read(512)
        file.stream.seek(0)
        detected = cls._detected_type(header)
        normalized = "jpg" if extension in {"jpg", "jpeg"} else extension
        if detected != normalized:
            raise ValueError("เนื้อหาไฟล์รูปภาพไม่ตรงกับชนิดไฟล์")
        return normalized

    @classmethod
    def attach_images(cls, repair: RepairRequest, files, image_type: str) -> list[RepairImage]:
        kind = ImageType(image_type)
        upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
        upload_dir.mkdir(parents=True, exist_ok=True)
        created = []
        saved_paths = []
        try:
            for file in files:
                if not file or not file.filename:
                    continue
                extension = cls.validate(file)
                filename = f"{uuid.uuid4().hex}.{extension}"
                target = upload_dir / filename
                file.save(target)
                saved_paths.append(target)
                image = RepairImage(repair=repair, image_type=kind, image_path=f"uploads/{filename}")
                db.session.add(image)
                created.append(image)
        except Exception:
            for path in saved_paths:
                path.unlink(missing_ok=True)
            raise
        return created
