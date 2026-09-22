import csv
import io

from localization import problem_type_label, status_label, urgency_label


class ExportService:
    HEADERS = [
        "เลขที่ใบแจ้งซ่อม", "ผู้แจ้ง", "อาคาร", "ห้อง", "ประเภทปัญหา", "ความเร่งด่วน",
        "สถานะ", "เจ้าหน้าที่ซ่อม", "ค่าใช้จ่าย", "วันที่สร้าง", "วันที่ซ่อมเสร็จ",
    ]

    @classmethod
    def repairs_csv(cls, repairs) -> str:
        output = io.StringIO()
        output.write("\ufeff")
        writer = csv.writer(output)
        writer.writerow(cls.HEADERS)
        for repair in repairs:
            writer.writerow([
                repair.request_no,
                repair.reporter.fullname,
                repair.building,
                repair.room,
                problem_type_label(repair.problem_type),
                urgency_label(repair.urgency),
                status_label(repair.status),
                repair.technician.fullname if repair.technician else "",
                repair.cost if repair.cost is not None else "",
                repair.created_at.isoformat(sep=" ", timespec="minutes"),
                repair.completion_date.isoformat() if repair.completion_date else "",
            ])
        return output.getvalue()
