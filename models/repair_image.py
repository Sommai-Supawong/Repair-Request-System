from datetime import datetime, timezone

from enums import ImageType
from extensions import db


class RepairImage(db.Model):
    __tablename__ = "repair_images"

    id = db.Column(db.Integer, primary_key=True)
    repair_id = db.Column(db.Integer, db.ForeignKey("repair_requests.id"), nullable=False, index=True)
    image_type = db.Column(db.Enum(ImageType, values_callable=lambda e: [x.value for x in e]), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    repair = db.relationship("RepairRequest", back_populates="images")

