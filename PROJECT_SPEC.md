# School Repair Management System

### ระบบแจ้งซ่อมภายในโรงเรียน

โปรเจกต์นี้เป็น Web Application สำหรับจัดการงานแจ้งซ่อมภายในโรงเรียน ตั้งแต่ครู/บุคลากรแจ้งปัญหา ผู้ดูแลมอบหมายช่าง ช่างรับงานและอัปเดตสถานะ ไปจนถึงบันทึกผลการซ่อม ค่าใช้จ่าย รูปก่อน-หลังซ่อม และเก็บประวัติย้อนหลัง โดยใบงานกำหนดแนวทางหลักเป็น Python, Flask, SQLite และแนวคิด OOAD/OOP 

---

## 1. เป้าหมายของระบบ

ปัญหาหลักที่ระบบต้องแก้คือ งานแจ้งซ่อมภายในโรงเรียนมักกระจัดกระจาย ไม่ทราบว่าใครรับผิดชอบ ไม่รู้สถานะปัจจุบัน และไม่มีประวัติย้อนหลัง เช่น ไฟเสีย แอร์ไม่เย็น หรือคอมพิวเตอร์ใช้งานไม่ได้ 

ดังนั้นระบบต้องสามารถจัดการวงจรงานทั้งหมดได้แบบ:

```text
แจ้งปัญหา
   ↓
รับเรื่อง
   ↓
มอบหมายช่าง
   ↓
ดำเนินการซ่อม
   ↓
บันทึกผล
   ↓
ปิดงาน
   ↓
เก็บประวัติย้อนหลัง
```

---

# 2. Technology Stack

ตามแนวทางของใบงาน ระบบใช้เทคโนโลยีหลักดังนี้ 

```text
Backend
- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-Login

Database
- SQLite

Frontend
- HTML
- CSS
- Jinja2
- Bootstrap
- JavaScript
- SweetAlert2

File Management
- Werkzeug secure_filename()
- Local Upload Folder

Export
- Python csv module
- WeasyPrint หรือ pdfkit

Testing
- pytest
```

### Dependencies ที่แนะนำ

```txt
Flask
Flask-SQLAlchemy
Flask-Login
Flask-WTF
Flask-Migrate
Werkzeug
python-dotenv
WeasyPrint
pytest
```

โดย `Flask-WTF`, `Flask-Migrate`, `python-dotenv` และ `pytest` เป็นส่วนที่ผมแนะนำเพิ่มเติมสำหรับระบบจริง ไม่ได้ถูกบังคับโดยใบงานโดยตรง

---

# 3. User Roles

ระบบมีผู้ใช้งาน 3 ประเภทตาม Requirement 

| Role       | หน้าที่                                   |
| ---------- | ----------------------------------------- |
| Admin      | ดูแลระบบ ผู้ใช้ งานแจ้งซ่อม และมอบหมายงาน |
| Teacher    | แจ้งซ่อมและติดตามงาน                      |
| Technician | รับงาน ซ่อม และอัปเดตผล                   |

## Admin

ทำได้:

```text
Login
ดู Dashboard ทั้งระบบ
ดูใบแจ้งซ่อมทั้งหมด
ค้นหา / Filter
มอบหมาย Technician
กำหนด Due Date
จัดการผู้ใช้
ดู Comment
ดูรูปก่อน/หลัง
Export CSV
Print / PDF
```

---

## Teacher / บุคลากร

ทำได้:

```text
Login
สร้างใบแจ้งซ่อม
เลือกอาคาร
เลือกห้อง
เลือกประเภทปัญหา
ระบุรายละเอียด
เลือกระดับความเร่งด่วน
แนบรูปก่อนซ่อม
ดูงานที่ตัวเองแจ้ง
ติดตามสถานะ
เพิ่ม Comment
ดูผลการซ่อม
```

---

## Technician

ทำได้:

```text
Login
ดูงานที่ได้รับมอบหมาย
รับงาน
เริ่มซ่อม
อัปเดตสถานะ
เพิ่ม Comment
บันทึกผลการซ่อม
บันทึกค่าใช้จ่าย
แนบรูปหลังซ่อม
ปิดงาน
```

---

# 4. Main Features

ใบงานกำหนด Feature หลักดังนี้ 

```text
Authentication / Authorization
Repair Request
Repair Assignment
Repair Tracking
Before / After Images
Comment System
Repair Result
Repair Cost
Dashboard
Search
Filter
CSV Export
Print
PDF Export
```

---

# 5. Workflow

สถานะของ Repair Request มี 4 State หลัก 

```text
PENDING
   ↓
ACCEPTED
   ↓
IN_PROGRESS
   ↓
COMPLETED
```

ความหมาย:

```text
pending
= ครูแจ้งเรื่องแล้ว แต่ยังไม่มีการรับงาน

accepted
= Admin มอบหมาย Technician แล้ว

in_progress
= Technician เริ่มดำเนินการซ่อม

completed
= ซ่อมเสร็จและบันทึกผลเรียบร้อย
```

Business Rule สำคัญ:

```text
pending
ไม่ควรข้ามไป in_progress

accepted
เท่านั้นที่สามารถ start_repair()

in_progress
เท่านั้นที่ควร complete_repair()
```

---

# 6. OOP / OOAD Design

## Main Classes

จากการสกัดคำนามและโครงสร้างข้อมูล ควรมี Model หลักอย่างน้อย:

```python
User
RepairRequest
RepairImage
Comment
```

และใช้ Enum สำหรับค่าที่มีชุดจำกัด เช่น:

```python
UserRole
RequestStatus
ProblemType
Urgency
ImageType
```

---

# 7. User Class

ตัวอย่าง Attribute:

```python
class User:
    id
    username
    password_hash
    fullname
    role
    email
    created_at
```

Responsibilities:

```text
เก็บข้อมูลผู้ใช้
Authentication
ตรวจสอบ Role
เชื่อมโยง RepairRequest
เชื่อมโยง Comment
เชื่อมโยง Assignment
```

---

# 8. RepairRequest Class

เป็น Domain Class หลักของระบบ ตัวอย่างในโจทย์กำหนด Attribute เช่น `request_no`, อาคาร, ห้อง, ประเภทปัญหา, ความเร่งด่วน, สถานะ, ผู้รับผิดชอบ และค่าใช้จ่าย 

แนะนำให้ใช้:

```python
@dataclass
class RepairRequest:
    id: int | None
    request_no: str

    user_id: int

    building: str
    room: str

    problem_type: ProblemType
    description: str

    urgency: Urgency

    status: RequestStatus

    assigned_to: int | None

    due_date: date | None
    completion_date: date | None

    cost: float | None
    result: str | None

    created_at: datetime
```

Methods:

```python
assign_to()
start_repair()
complete_repair()
```

ตัวอย่าง Logic:

```python
def assign_to(self, technician_id, due_date):
    self.assigned_to = technician_id
    self.due_date = due_date
    self.status = RequestStatus.ACCEPTED
```

```python
def start_repair(self):
    if self.status != RequestStatus.ACCEPTED:
        raise ValueError("Request must be accepted first")

    self.status = RequestStatus.IN_PROGRESS
```

```python
def complete_repair(self, cost, result):
    if self.status != RequestStatus.IN_PROGRESS:
        raise ValueError("Repair is not in progress")

    self.cost = cost
    self.result = result
    self.completion_date = date.today()
    self.status = RequestStatus.COMPLETED
```

---

# 9. Enum

## RequestStatus

```python
class RequestStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
```

## ProblemType

ใบงานกำหนดประเภทปัญหาไว้ดังนี้ 

```python
class ProblemType(Enum):
    ELECTRICAL = "electrical"
    FURNITURE = "furniture"
    COMPUTER = "computer"
    AIRCON = "aircon"
    OTHER = "other"
```

## Urgency

```python
class Urgency(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
```

## ImageType

```python
class ImageType(Enum):
    BEFORE = "before"
    AFTER = "after"
```

---

# 10. Database

ระบบมี 4 ตารางหลักตาม Database Design ของใบงาน 

```text
users
repair_requests
repair_images
comments
```

---

# 11. Table: users

```text
users
├── id
├── username
├── password_hash
├── fullname
├── role
├── email
└── created_at
```

Constraint:

```sql
role IN (
    'admin',
    'teacher',
    'technician'
)
```

---

# 12. Table: repair_requests

```text
repair_requests
├── id
├── request_no
├── user_id
├── building
├── room
├── problem_type
├── description
├── urgency
├── status
├── assigned_to
├── due_date
├── completion_date
├── cost
├── result
└── created_at
```

Foreign Keys:

```text
user_id
→ users.id

assigned_to
→ users.id
```

---

# 13. Table: repair_images

```text
repair_images
├── id
├── repair_id
├── image_type
├── image_path
└── uploaded_at
```

โดย

```text
image_type =
before
after
```

เหตุผลที่แยกตารางออกจาก `repair_requests` คือใบแจ้งซ่อมหนึ่งรายการสามารถมีหลายรูป จึงเป็นความสัมพันธ์ 1:N และยืดหยุ่นกว่าการสร้าง `image1`, `image2`, `image3` ในตารางหลัก 

---

# 14. Table: comments

```text
comments
├── id
├── repair_id
├── user_id
├── comment
└── created_at
```

---

# 15. Database Relationships

```text
User
 │
 │ 1
 │
 └────────── N RepairRequest
                    │
                    ├──── 1:N ─── RepairImage
                    │
                    └──── 1:N ─── Comment
                                     │
                                     N
                                     │
                                     1
                                    User
```

Relationships:

```text
User 1:N RepairRequest
User 1:N Assigned RepairRequest
RepairRequest 1:N RepairImage
RepairRequest 1:N Comment
User 1:N Comment
```

---

# 16. Request Number

รูปแบบรหัสใบแจ้งซ่อมตามโจทย์:

```text
RP-YYYYMM-XXX
```

ตัวอย่าง:

```text
RP-202609-001
RP-202609-002
RP-202609-003
```

Function:

```python
def generate_request_no(sequence: int) -> str:
    now = datetime.now()

    year_month = now.strftime("%Y%m")

    running_number = str(sequence).zfill(3)

    return f"RP-{year_month}-{running_number}"
```

ระบบจริงควรหา Running Number จาก Database ไม่ควรให้ผู้ใช้กำหนดเอง

---

# 17. Application Architecture

ผมแนะนำโครงสร้างแบบแยก Layer เพื่อให้อ่านง่ายและคงหลัก OOAD/OOP

```text
Presentation
    ↓
Route / Controller
    ↓
Service
    ↓
Model / Repository
    ↓
Database
```

ตัวอย่าง:

```text
HTML / Jinja2
      ↓
repair_routes.py
      ↓
repair_service.py
      ↓
RepairRequest
      ↓
SQLAlchemy
      ↓
SQLite
```

---

# 18. Recommended Folder Structure

```text
school-repair-system/
│
├── app.py
├── config.py
├── extensions.py
│
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── instance/
│   └── repair.db
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── repair_request.py
│   ├── repair_image.py
│   └── comment.py
│
├── enums/
│   ├── user_role.py
│   ├── request_status.py
│   ├── problem_type.py
│   ├── urgency.py
│   └── image_type.py
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── repairs.py
│   └── admin.py
│
├── services/
│   ├── repair_service.py
│   ├── user_service.py
│   ├── upload_service.py
│   └── export_service.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   │
│   ├── dashboard/
│   │   └── index.html
│   │
│   ├── repairs/
│   │   ├── list.html
│   │   ├── create.html
│   │   ├── detail.html
│   │   └── print.html
│   │
│   └── admin/
│       └── users.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── main.js
│   │
│   └── uploads/
│
└── tests/
    ├── test_auth.py
    ├── test_repairs.py
    ├── test_permissions.py
    └── test_status.py
```

---

# 19. Main Pages

ใบงานกำหนดหน้าจอหลักของระบบดังนี้ 

### Login

```text
/login
```

มี:

```text
Username
Password
Login Button
```

---

### Dashboard

```text
/dashboard
```

ทุก Role เข้าถึงได้ แต่ข้อมูลต้อง Filter ตามสิทธิ์

แสดง:

```text
Total Repairs
Pending
Accepted
In Progress
Completed
```

อาจเพิ่ม:

```text
High Priority
Overdue
Recent Repairs
My Tasks
```

สองตัวหลังเป็นข้อเสนอเพิ่มเติมสำหรับระบบจริง

---

# 20. Create Repair Page

```text
/repair/create
```

สำหรับ:

```text
Teacher
Admin
```

Form:

```text
Building *
Room *

Problem Type *
- Electrical
- Furniture
- Computer
- Air Conditioner
- Other

Urgency *
- Low
- Medium
- High

Description *

Before Repair Images

Submit
Cancel
```

---

# 21. Repair List

```text
/repairs
```

แสดง:

```text
Request No
Reporter
Building
Room
Problem Type
Urgency
Status
Technician
Created Date
```

Search:

```text
Request No
Building
Room
Description
```

Filter:

```text
Status
Urgency
Problem Type
Technician
Date
```

---

# 22. Repair Detail

```text
/repair/<id>
```

แสดง:

```text
Request No
Reporter
Location
Problem
Description
Urgency
Status

Assigned Technician
Due Date

Before Images
After Images

Repair Result
Cost
Completion Date

Comments
```

Action ตาม Role เช่น:

```text
Admin
→ Assign Technician

Technician
→ Start Repair
→ Complete Repair

All authorized users
→ Add Comment
```

---

# 23. Admin User Management

```text
/admin/users
```

Admin only

ทำได้:

```text
View Users
Create User
Edit User
Delete / Disable User
Change Role
```

---

# 24. Authentication

ใช้ Flask-Login ตาม Coding Exercise ของใบงาน 

ตัวอย่าง:

```python
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
```

Login:

```python
login_user(user)
```

Logout:

```python
logout_user()
```

Protected Route:

```python
@login_required
def dashboard():
    ...
```

---

# 25. Authorization

ไม่ควรตรวจแค่ว่า Login แล้วหรือไม่ แต่ต้องตรวจ Role ด้วย

ตัวอย่าง:

```python
if current_user.role != "admin":
    abort(403)
```

หรือสร้าง Decorator:

```python
@roles_required("admin")
```

และ:

```python
@roles_required(
    "admin",
    "technician"
)
```

---

# 26. Dashboard Logic

ใบงานกำหนด Dashboard ต้องนับจำนวนงานทั้งหมด งานรอ งานกำลังดำเนินการ และงานเสร็จแล้ว 

ตัวอย่าง:

```python
stats = {
    "total": RepairRequest.query.count(),

    "pending":
        RepairRequest.query.filter_by(
            status="pending"
        ).count(),

    "in_progress":
        RepairRequest.query.filter_by(
            status="in_progress"
        ).count(),

    "completed":
        RepairRequest.query.filter_by(
            status="completed"
        ).count(),
}
```

---

# 27. File Upload

ใบงานกำหนดให้รองรับรูปก่อนและหลังซ่อม และใช้ `secure_filename()` 

Allowed Files:

```text
.jpg
.jpeg
.png
.gif
```

ควร:

```python
secure_filename()
```

และสร้างชื่อใหม่ด้วย:

```python
uuid.uuid4()
```

ตัวอย่าง:

```text
/uploads/
    a930b4...jpg
    b68a29...png
```

ไม่ควรเก็บชื่อเดิมจาก User ตรง ๆ

---

# 28. Upload Security

ใบงานระบุข้อควรระวังของระบบ Upload ไว้ เช่น `secure_filename`, MIME checking, file-size limit และการเปลี่ยนชื่อไฟล์ 

ควรตั้ง:

```python
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
```

ประมาณ:

```text
5 MB / file
```

และตรวจ:

```text
Extension
MIME Type
File Size
Filename
Permission
```

---

# 29. Comment System

ทุก Comment ต้องสัมพันธ์กับ:

```text
RepairRequest
User
```

Flow:

```text
User เปิดใบแจ้งซ่อม
↓
พิมพ์ Comment
↓
POST
↓
บันทึก
↓
แสดง Timeline
```

UI:

```text
Somchai
22 Sep 2026 10:21
"ตรวจสอบเบื้องต้นแล้ว พบ Compressor มีปัญหา"
```

---

# 30. SweetAlert2

ใบงานต้องการ Notification เมื่อ 

```text
แจ้งซ่อมสำเร็จ
มอบหมายงานสำเร็จ
อัปเดตสถานะสำเร็จ
```

Flask:

```python
flash(
    "แจ้งซ่อมสำเร็จ",
    "success"
)
```

Jinja2:

```javascript
Swal.fire({
    icon: "success",
    title: "แจ้งซ่อมสำเร็จ"
})
```

---

# 31. CSV Export

Admin สามารถ Export รายการแจ้งซ่อมเป็น:

```text
repairs.csv
```

Column ตัวอย่าง:

```text
Request No
Reporter
Building
Room
Problem Type
Urgency
Status
Technician
Cost
Created At
Completed At
```

ใช้ Python:

```python
csv
```

---

# 32. PDF / Print

ใบงานกำหนด Bonus เป็นการ Export PDF ด้วย WeasyPrint หรือ pdfkit 

แนะนำ:

```text
Jinja2 Template
↓
HTML
↓
WeasyPrint
↓
PDF
```

ตัวอย่างชื่อไฟล์:

```text
RP-202609-001.pdf
```

หรือรองรับ Browser Print:

```javascript
window.print()
```

---

# 33. UI Design

แนวทาง UI จากใบงานคือ:

```text
Bootstrap
Responsive
Clean
Simple
Readable
```

Pages ควรใช้ Layout เดียวกัน:

```text
Sidebar
Navbar
Content
Cards
Table
Modal / SweetAlert
```

Dashboard:

```text
┌────────────┐
│ Total 124  │
└────────────┘

┌────────────┐
│ Pending 12 │
└────────────┘

┌───────────────┐
│ In Progress 8 │
└───────────────┘

┌───────────────┐
│ Completed 104 │
└───────────────┘
```

---

# 34. Validation

Frontend + Backend ต้องตรวจทั้งคู่

ตัวอย่าง:

```text
Building required
Room required
Problem Type required
Description required
Urgency required
```

Cost:

```text
>= 0
```

File:

```text
extension valid
size <= limit
```

Status:

```text
must follow State Transition
```

---

# 35. Security

สำหรับระบบจริงควรมี:

```text
Password Hashing
Session Authentication
Role Authorization
CSRF Protection
Input Validation
Secure File Upload
SQL Injection Protection
XSS Prevention
Secret Key from Environment
Upload Size Limit
```

Password:

```python
generate_password_hash()
check_password_hash()
```

ห้ามเก็บ:

```text
password = "123456"
```

แบบ Plain Text

---

# 36. Environment Variables

`.env`

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///repair.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=5242880
```

และ:

```text
.env
```

ต้องใส่ใน `.gitignore`

---

# 37. Recommended `.gitignore`

```gitignore
__pycache__/
*.pyc

.env

instance/
*.db

static/uploads/*

.pytest_cache/

venv/
.venv/

.DS_Store
```

---

# 38. Development Sequence

แนะนำสร้างตามลำดับนี้

1. **Project Setup**

```text
Flask
Folder Structure
Config
Database
```

2. **Models**

```text
User
RepairRequest
RepairImage
Comment
Enums
```

3. **Database**

```text
Relationships
Constraints
Seed Users
```

4. **Authentication**

```text
Login
Logout
Session
Role
```

5. **Repair CRUD**

```text
Create
Read
List
Search
Filter
```

6. **Assignment**

```text
Admin
→ Technician
```

7. **State Workflow**

```text
pending
accepted
in_progress
completed
```

8. **Upload**

```text
Before Image
After Image
```

9. **Comments**

10. **Dashboard**

11. **SweetAlert2**

12. **CSV Export**

13. **PDF**

14. **Testing**

15. **README**

16. **Screenshots**

---

# 39. Test Cases

อย่างน้อยควร Test:

### Authentication

```text
Login ถูก
Login ผิด
Logout
เข้า Protected Route โดยไม่ Login
```

### Authorization

```text
Teacher เข้า Admin page → 403

Technician สร้าง User → 403

Teacher ดู Repair ของคนอื่น
→ ต้องถูกจำกัดตาม Requirement
```

### Repair

```text
Create Repair

Missing Building
→ Error

Invalid Problem Type
→ Error
```

### Status

```text
pending → accepted
PASS

accepted → in_progress
PASS

in_progress → completed
PASS

pending → completed
FAIL
```

### Upload

```text
.jpg
PASS

.png
PASS

.exe
FAIL

file > 5MB
FAIL
```

---

# 40. Seed Accounts

สำหรับ Demo สามารถเตรียม:

```text
Admin

username:
admin

role:
admin
```

```text
Teacher

username:
teacher01

role:
teacher
```

```text
Technician

username:
tech01

role:
technician
```

รหัสผ่านจริงต้อง Hash ก่อนบันทึก

---

# 41. Demo Scenario

กรณี Demo ที่ดี:

```text
Teacher Login
↓
แจ้งว่า
"แอร์ห้อง 301 ไม่เย็นและมีเสียงดัง"
↓
Urgency = High
↓
Upload Before Image
↓
Submit
```

ได้:

```text
RP-202609-001
```

จากนั้น:

```text
Admin Login
↓
Assign tech01
↓
Due Date = 25/09/2026
```

สถานะ:

```text
accepted
```

Technician:

```text
Login
↓
Start Repair
```

เป็น:

```text
in_progress
```

จากนั้นบันทึก:

```text
Result:
ล้างแอร์และเติมสารทำความเย็น

Cost:
1500 บาท

Upload After Image
```

สุดท้าย:

```text
completed
```

Scenario นี้สอดคล้องกับตัวอย่าง `RepairRequest` ที่ให้ไว้ในใบงาน 

---

# 42. สิ่งที่ต้องส่ง

ใบงานกำหนด Deliverables หลักไว้ดังนี้ 

```text
Python Source Code
.py

requirements.txt

SQLite Database
.db หรือ schema.sql

HTML / Jinja2 Templates

README.md

Screenshots
```

และควรมีโครงสร้างประมาณ:

```text
school-repair-system.zip
│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
├── routes/
├── services/
│
├── templates/
├── static/
│
├── instance/
│   └── repair.db
│
└── screenshots/
```

---

# 43. Evaluation Focus

จากเกณฑ์คะแนน งานให้ความสำคัญกับ Backend Python และ Functionality ค่อนข้างมาก โดยแบ่งเป็น Requirements 15, Database 20, Python Backend 25, UI/UX 15, Features 20 และ Documentation 5 คะแนน 

ดังนั้นอย่าทุ่มเวลาให้ UI จน Business Logic ไม่ครบ

สิ่งที่ต้องให้ความสำคัญก่อนคือ:

```text
OOP
Database
Role
Login
Repair Workflow
Upload
Dashboard
Security
```

แล้วค่อยปรับ UI ให้สวย

---

# 44. MVP ที่ถือว่าระบบใช้งานได้

ถ้าจะทำ Version แรกให้เสร็จเร็วที่สุด:

```text
✓ Login

✓ 3 Roles

✓ Create Repair

✓ Repair List

✓ Repair Detail

✓ Assign Technician

✓ Status Update

✓ Repair Result

✓ Cost

✓ Before / After Image

✓ Comment

✓ Dashboard

✓ SweetAlert2
```

หลังจาก MVP เสร็จจึงเพิ่ม:

```text
CSV
PDF
Advanced Search
Advanced Dashboard
Tests
Deployment
```

---

# 45. Definition of Done

โปรเจกต์ถือว่าเสร็จเมื่อ Flow นี้ทำงานได้จริง:

```text
Teacher Login
↓
Create Repair
↓
Admin เห็นงาน
↓
Admin Assign Technician
↓
Technician เห็นงาน
↓
Technician Start Repair
↓
Upload / Comment
↓
Complete Repair
↓
Teacher เห็น Completed
↓
Admin Dashboard Update
↓
Export CSV / PDF
```

และต้องไม่มี User Role ไหนสามารถเข้าถึง Function ที่ไม่มีสิทธิ์ได้

---

## สรุปภาพรวม Architecture

```text
                   ┌─────────────┐
                   │    User     │
                   └──────┬──────┘
                          │
                  Flask + Jinja2
                          │
             ┌────────────▼─────────────┐
             │        Routes            │
             │ Auth / Repair / Admin    │
             └────────────┬─────────────┘
                          │
             ┌────────────▼─────────────┐
             │        Services          │
             │ Repair / Upload / Export │
             └────────────┬─────────────┘
                          │
             ┌────────────▼─────────────┐
             │        Models            │
             │ User                     │
             │ RepairRequest            │
             │ RepairImage              │
             │ Comment                  │
             └────────────┬─────────────┘
                          │
                   SQLAlchemy ORM
                          │
                   ┌──────▼──────┐
                   │   SQLite    │
                   └─────────────┘
```

**แก่นของโปรเจกต์นี้จริง ๆ คือ** การสร้างระบบ Workflow Management ขนาดเล็กที่ใช้ OOP ควบคุม Business Logic โดยมี `RepairRequest` เป็น Domain หลัก, `User` จัดการสิทธิ์, `RepairImage` เก็บหลักฐาน และ `Comment` ใช้สื่อสารระหว่างผู้เกี่ยวข้อง พร้อม State Transition ที่ชัดเจนตั้งแต่ `pending → accepted → in_progress → completed` ครับ.
