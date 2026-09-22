Read the entire existing project, including `PROJECT_SPEC.md`, current templates, CSS, JavaScript, routes, models, and existing UI before making changes.

Your task is to **redesign and improve the existing School Repair Management System UI/UX** to make it significantly more:

* User-friendly
* Minimal
* Clean
* Soft
* Easy to understand
* Suitable for Thai users
* Suitable for teachers, staff, technicians, and administrators
* Responsive on desktop, tablet, and mobile

The application already has working business logic.

Do NOT rebuild the project from scratch.

Do NOT change the existing database structure, authentication logic, role permissions, repair workflow, routes, models, or other backend behavior unless a UI integration issue requires a very small safe adjustment.

The main goal is:

`Existing working functionality + better Thai UX + minimal soft UI + fully responsive design`

---

# 1. DESIGN DIRECTION

Redesign the application using a:

**Minimal Soft UI / Clean Administration UI**

The result should feel:

* Modern
* Friendly
* Calm
* Professional
* Easy for non-technical users
* Appropriate for Thai school staff
* Clear even for first-time users

Avoid making the application look like:

* A complex enterprise dashboard
* A developer/admin template
* A futuristic AI interface
* A gaming UI
* A financial trading dashboard
* A flashy SaaS landing page

The system is an internal repair-management tool.

Usability is more important than visual effects.

---

# 2. STRICTLY NO GRADIENTS

Do NOT use gradients anywhere.

Do not use:

```css
linear-gradient()
radial-gradient()
conic-gradient()
```

Avoid gradient:

* backgrounds
* buttons
* cards
* sidebar
* navbar
* status badges
* decorative elements

Use solid colors only.

---

# 3. COLOR SYSTEM

Use a clean neutral palette with a calm primary color.

Suggested direction:

```text
Background:
#F6F7F9

Surface:
#FFFFFF

Primary:
#2563EB

Primary Hover:
#1D4ED8

Primary Soft:
#EFF6FF

Text Primary:
#1F2937

Text Secondary:
#6B7280

Border:
#E5E7EB

Soft Border:
#EEF0F3
```

Status colors:

```text
Pending:
soft gray / amber

Accepted:
soft blue

In Progress:
soft orange

Completed:
soft green
```

Urgency:

```text
Low:
green

Medium:
amber

High:
red
```

Colors should be muted enough for long-term daily use.

Do not overuse the primary blue.

Most of the interface should remain neutral.

---

# 4. SOFT UI STYLE

Use Soft UI carefully.

Soft UI means:

* Light background
* White cards
* Soft shadows
* Rounded corners
* Comfortable spacing
* Clear hierarchy
* Subtle hover states

It does NOT mean excessive neumorphism.

Avoid deeply embossed neumorphic controls.

Use subtle shadows such as:

```css
box-shadow:
0 1px 2px rgba(0,0,0,0.04),
0 4px 16px rgba(0,0,0,0.04);
```

Suggested border radius:

```text
Cards:
14–18px

Buttons:
10–12px

Inputs:
10–12px

Badges:
999px
```

Do not make every element excessively rounded.

---

# 5. TYPOGRAPHY FOR THAI

Thai readability is extremely important.

Use:

```css
font-family:
"Sarabun",
"Noto Sans Thai",
system-ui,
sans-serif;
```

Prefer Sarabun if already available.

Typography hierarchy:

```text
Page title:
28–32px desktop
24–26px mobile

Section title:
18–22px

Body:
14–16px

Labels:
14px

Small metadata:
12–13px
```

Use comfortable Thai line-height:

```css
line-height: 1.6;
```

Avoid:

* Tiny Thai text
* Very light font weights
* Extremely bold fonts everywhere
* Uppercase English styling applied to Thai

---

# 6. THAI-FIRST UX

The web interface must be designed primarily for Thai users.

All important user-facing content should already be Thai according to the existing localization.

Review the wording again and make sure labels are natural.

Prefer simple wording.

Example:

Instead of:

`ดำเนินการสร้างคำร้องแจ้งซ่อม`

use:

`แจ้งซ่อมใหม่`

Instead of:

`ดำเนินการมอบหมายผู้รับผิดชอบ`

use:

`มอบหมายเจ้าหน้าที่`

Instead of:

`ย้อนกลับไปยังรายการ`

use:

`กลับ`

Use terminology consistently throughout the application.

---

# 7. MAIN APPLICATION LAYOUT

Desktop should use a simple application shell:

```text
┌──────────────┬──────────────────────────────┐
│              │ Top Bar                      │
│   Sidebar    ├──────────────────────────────┤
│              │                              │
│              │ Main Content                 │
│              │                              │
└──────────────┴──────────────────────────────┘
```

Keep navigation minimal.

Suggested desktop sidebar:

```text
ระบบแจ้งซ่อม

ภาพรวม
แจ้งซ่อมใหม่
รายการแจ้งซ่อม

ADMIN ONLY
จัดการผู้ใช้งาน

บัญชีของฉัน
ออกจากระบบ
```

Do not display navigation links that the user's role cannot access.

---

# 8. SIDEBAR

Desktop:

* Width approximately 240–260px
* White or very light neutral surface
* Thin right border
* No dark sidebar
* No gradient
* Clear active state
* Simple icons
* Good Thai text spacing

Active item example:

```text
soft blue background
blue icon
blue/dark text
```

Avoid huge colorful navigation buttons.

Icons should be secondary to labels.

Use a consistent icon library already available in the project.

Do not introduce multiple icon libraries.

---

# 9. MOBILE NAVIGATION

Do not simply shrink the desktop sidebar.

For screens below approximately:

```text
768px
```

Convert sidebar to either:

* Drawer navigation

or preferably for main actions:

* Compact mobile header + drawer

Keep important actions easy to reach.

Mobile header example:

```text
[☰] ระบบแจ้งซ่อม              [Profile]
```

Make touch targets at least approximately:

```text
44px
```

---

# 10. TOP BAR

Keep the top bar minimal.

Desktop example:

```text
หน้าปัจจุบัน

                         Somchai
                         ครู / บุคลากร
                         [avatar]
```

Do not fill the top bar with unnecessary information.

Possible contents:

* Current page title
* User name
* Role
* Profile/avatar
* Mobile menu button

Avoid:

* Large search bar on every page
* Excessive icons
* Notifications if the system does not actually support them

---

# 11. DASHBOARD REDESIGN

Dashboard should immediately answer:

**“ตอนนี้งานซ่อมของฉัน/ระบบเป็นอย่างไร?”**

Do not overwhelm the user.

Top section:

```text
สวัสดี, คุณสมชาย

ภาพรวมงานแจ้งซ่อม
```

Statistics:

```text
งานทั้งหมด
รอรับเรื่อง
กำลังดำเนินการ
ซ่อมเสร็จแล้ว
```

Use four simple cards.

Example visual structure:

```text
┌─────────────────┐
│ งานทั้งหมด      │
│                 │
│      24         │
│ รายการ          │
└─────────────────┘
```

Cards should:

* Use white surface
* Subtle border
* Very subtle shadow
* Small icon if useful
* Large number
* Clear Thai label

Do not use:

* Gradients
* Huge charts
* Decorative visualizations without value

---

# 12. ROLE-SPECIFIC DASHBOARD

Optimize the Dashboard for each role.

## Teacher

Prioritize:

```text
[ + แจ้งซ่อมใหม่ ]

งานของฉัน
รอรับเรื่อง
กำลังซ่อม
เสร็จแล้ว

รายการแจ้งซ่อมล่าสุด
```

The primary CTA should be:

**แจ้งซ่อมใหม่**

Make this action obvious.

---

## Technician

Prioritize:

```text
งานที่ได้รับมอบหมาย
งานที่ต้องทำวันนี้
กำลังดำเนินการ
งานเสร็จแล้ว

รายการงานของฉัน
```

Primary actions should clearly show:

```text
ดูงาน
เริ่มซ่อม
บันทึกผล
```

---

## Admin

Prioritize:

```text
งานทั้งหมด
รอรับเรื่อง
กำลังดำเนินการ
เสร็จแล้ว

รายการที่ยังไม่ได้มอบหมาย
รายการล่าสุด
```

Important CTA:

```text
มอบหมายเจ้าหน้าที่
```

---

# 13. REPAIR LIST REDESIGN

Desktop should use a clean table.

Do not overload columns.

Recommended columns:

```text
เลขที่
สถานที่
ประเภทปัญหา
ความเร่งด่วน
สถานะ
ผู้รับผิดชอบ
วันที่แจ้ง
จัดการ
```

Reporter may be shown only where relevant.

Use badges for:

* status
* urgency

Example:

```text
รอรับเรื่อง
กำลังดำเนินการ
ซ่อมเสร็จแล้ว
```

Do not display database values such as:

```text
in_progress
completed
```

directly to users.

---

# 14. MOBILE REPAIR LIST

This is important.

Do NOT force the desktop table into a horizontally scrolling tiny layout unless absolutely necessary.

On mobile, convert repair rows into cards.

Example:

```text
┌─────────────────────────────┐
│ RP-202609-001      [ด่วนสูง]│
│                             │
│ เครื่องปรับอากาศ            │
│ อาคาร 3 · ห้อง 301          │
│                             │
│ [กำลังดำเนินการ]            │
│                             │
│ ผู้รับผิดชอบ: สมชาย         │
│                             │
│ 22 ก.ย. 2569        ดู >     │
└─────────────────────────────┘
```

Mobile users should be able to understand each repair without horizontal scrolling.

---

# 15. SEARCH AND FILTER UX

Desktop:

```text
[ 🔍 ค้นหาเลขที่ / ห้อง / รายละเอียด... ]

[สถานะ ▼] [ความเร่งด่วน ▼] [ประเภท ▼]

[ล้างตัวกรอง]
```

Mobile:

Use:

```text
[ 🔍 ค้นหา... ]

[ ตัวกรอง ]
```

The filter button may open a:

* Bottom sheet
* Modal
* Collapsible panel

Do not show five tiny dropdowns squeezed into one mobile row.

---

# 16. EMPTY STATES

Create proper empty states.

Example Teacher:

```text
ยังไม่มีรายการแจ้งซ่อม

เมื่อพบอุปกรณ์หรือสถานที่ชำรุด
คุณสามารถแจ้งปัญหาได้ที่นี่

[ + แจ้งซ่อมใหม่ ]
```

Technician:

```text
ยังไม่มีงานที่ได้รับมอบหมาย
```

Search:

```text
ไม่พบรายการที่ตรงกับการค้นหา
ลองเปลี่ยนคำค้นหาหรือตัวกรอง
```

Do not leave users looking at an empty table.

---

# 17. CREATE REPAIR PAGE

This is one of the most important UX flows.

Make the form easy for non-technical Thai users.

Instead of one long dense form, group information logically.

Example:

```text
แจ้งซ่อมใหม่

กรอกข้อมูลปัญหาที่พบ
เพื่อให้เจ้าหน้าที่สามารถตรวจสอบและดำเนินการได้เร็วขึ้น


1. สถานที่

อาคาร
[ เลือกหรือกรอกอาคาร ]

ห้อง
[ เช่น 301 ]


2. ปัญหาที่พบ

ประเภทปัญหา
[ เครื่องปรับอากาศ ▼ ]

รายละเอียดปัญหา
[ อธิบายสิ่งที่พบ... ]


3. ความเร่งด่วน

( ) ต่ำ
(•) ปานกลาง
( ) สูง


4. รูปภาพ

เพิ่มรูปก่อนซ่อม
[ + เพิ่มรูปภาพ ]


[ยกเลิก]                [ส่งใบแจ้งซ่อม]
```

---

# 18. FORM UX

All forms must have:

* Visible labels
* Helpful placeholders
* Clear required indicators
* Inline validation
* Good spacing
* Correct input types
* Clear focus states

Avoid floating labels if they hurt Thai readability.

Example:

```text
อาคาร *

[ อาคาร 3                 ]
```

is better than putting critical labels only inside placeholders.

---

# 19. VALIDATION

Validation errors should appear directly under the relevant field.

Example:

```text
รายละเอียดปัญหา *

[                              ]

กรุณากรอกรายละเอียดปัญหา
```

Use red carefully.

Do not show only a generic alert at the top when the error belongs to a specific field.

SweetAlert2 can still show overall success/error feedback.

---

# 20. BUTTON SYSTEM

Create consistent button styles.

## Primary

Use for one main action per area:

```text
ส่งใบแจ้งซ่อม
บันทึกผล
มอบหมายเจ้าหน้าที่
```

Solid primary blue.

## Secondary

Example:

```text
ยกเลิก
กลับ
```

White / neutral background + border.

## Destructive

Example:

```text
ลบผู้ใช้งาน
```

Use red only for destructive actions.

Do not use many different button colors.

---

# 21. REPAIR DETAIL PAGE

Make the repair detail page easy to scan.

Suggested hierarchy:

```text
RP-202609-001

[กำลังดำเนินการ]    [ความเร่งด่วนสูง]

เครื่องปรับอากาศ
อาคาร 3 · ห้อง 301
```

Then separate information into cards/sections:

```text
รายละเอียดปัญหา

ข้อมูลการแจ้ง

ผู้รับผิดชอบ

รูปก่อนซ่อม

ความคืบหน้า

ผลการซ่อม

ความคิดเห็น
```

Do not present everything in a giant table.

---

# 22. STATUS / PROGRESS UI

Since repair requests have a fixed workflow:

```text
รอรับเรื่อง
→ รับเรื่องแล้ว
→ กำลังดำเนินการ
→ ซ่อมเสร็จแล้ว
```

Create a simple progress indicator on the detail page.

Desktop:

```text
●────────●────────●────────○

รับเรื่อง    มอบหมาย      กำลังซ่อม      เสร็จ
```

Mobile can use a vertical progress list.

Keep it minimal.

No animations are required.

---

# 23. ACTION PRIORITY

Do not show every possible button with the same visual weight.

Example Technician in `accepted` state:

Primary action:

```text
เริ่มดำเนินการซ่อม
```

Secondary actions:

```text
เพิ่มความคิดเห็น
กลับ
```

After repair starts:

Primary:

```text
บันทึกผลการซ่อม
```

This reduces decision fatigue.

---

# 24. IMAGE UPLOAD UX

Make image upload friendly.

Use an upload area such as:

```text
┌─────────────────────────────┐
│                             │
│      + เพิ่มรูปภาพ          │
│                             │
│ JPG, PNG ไม่เกิน 5 MB       │
│                             │
└─────────────────────────────┘
```

After selection, show preview thumbnails.

Allow users to remove incorrectly selected images before submit where practical.

Do not expose internal file paths.

---

# 25. COMMENTS UX

Display comments as a simple activity thread.

Example:

```text
สมชาย ใจดี
เจ้าหน้าที่ซ่อม · 10:32

ตรวจสอบแล้ว พบว่าฟิลเตอร์แอร์อุดตัน
```

Avoid making comments look like a social-media chat application.

Keep the focus on work communication.

---

# 26. ADMIN USER MANAGEMENT

Keep Admin UI straightforward.

Desktop:

```text
ผู้ใช้งาน

[ + เพิ่มผู้ใช้งาน ]

[ ค้นหาผู้ใช้งาน... ]

ชื่อ
ชื่อผู้ใช้
อีเมล
สิทธิ์
วันที่สร้าง
จัดการ
```

Mobile:

Use cards instead of squeezing the full table.

Avoid exposing password fields after user creation.

---

# 27. LOGIN PAGE

Redesign Login to be very simple.

Desktop:

Use centered login card or subtle split layout.

Example:

```text
ระบบแจ้งซ่อมภายในโรงเรียน

เข้าสู่ระบบเพื่อจัดการและติดตามงานซ่อม

ชื่อผู้ใช้
[________________]

รหัสผ่าน
[________________]

[ เข้าสู่ระบบ ]
```

No gradient.

No giant illustration required.

No distracting animations.

Mobile should fit naturally without unnecessary scrolling.

---

# 28. RESPONSIVE BREAKPOINTS

Review the entire app for at least:

```text
Mobile:
320px – 767px

Tablet:
768px – 1023px

Desktop:
1024px+

Large Desktop:
1440px+
```

Do not optimize only for a 1920px monitor.

Test common widths:

```text
375px
390px
768px
1024px
1366px
1440px
```

---

# 29. MOBILE-FIRST REQUIREMENTS

On mobile:

* Forms must be full-width
* Cards should use available width
* Buttons should be easy to tap
* Primary submit button can become full-width
* Tables should turn into cards when appropriate
* Navigation should become drawer/mobile menu
* Avoid tiny icons
* Avoid tiny text
* Avoid horizontal page scrolling
* Modals must fit the viewport
* SweetAlert2 must remain usable
* Long Thai text must wrap correctly

---

# 30. CONTENT WIDTH

Do not stretch content endlessly on large monitors.

Suggested main content max width:

```css
max-width: 1440px;
```

Forms may be narrower:

```css
max-width: 760px;
```

Repair details:

```css
max-width: 1000px;
```

This improves readability.

---

# 31. SPACING SYSTEM

Use a consistent spacing system.

For example:

```text
4
8
12
16
24
32
40
48
```

Avoid random margins such as:

```text
13px
27px
37px
```

unless genuinely required.

Whitespace is an important part of this redesign.

---

# 32. ICONS

Use icons only when they improve comprehension.

Good examples:

```text
Dashboard
Repair
Search
User
Upload
Calendar
Comment
Logout
```

Avoid putting icons next to every piece of text.

Use a single consistent icon family.

Icons should be:

* simple
* outline or soft
* visually consistent

---

# 33. ACCESSIBILITY

Improve accessibility where practical.

Ensure:

* Adequate text contrast
* Visible keyboard focus state
* Buttons have readable labels
* Inputs have labels
* Images have alt text
* Icon-only controls have accessible labels
* Status is not communicated using color alone
* Touch targets are sufficiently large

---

# 34. HOVER / MOTION

Keep animation subtle.

Allowed:

```text
150–200ms
```

Examples:

* Button background transition
* Card hover shadow
* Sidebar active/hover state
* Dropdown transition

Avoid:

* bouncing
* glowing
* 3D rotation
* large entrance animation
* scroll animation
* parallax
* excessive motion

This is a productivity system.

---

# 35. REMOVE VISUAL CLUTTER

Review existing pages and remove unnecessary:

* Decorative containers
* Repeated titles
* Excessive icons
* Duplicate information
* Strong shadows
* Thick borders
* Multiple accent colors
* Excessive badges
* Unnecessary animations

Every UI element should have a reason to exist.

---

# 36. CSS ARCHITECTURE

Refactor CSS where necessary.

Avoid a giant collection of random page-specific styles.

Create reusable design tokens/components for:

```text
Colors
Typography
Spacing
Radius
Shadows

Button
Card
Badge
Input
Table
Sidebar
Navbar
Empty State
Page Header
```

Example:

```css
:root {
    --bg: #f6f7f9;
    --surface: #ffffff;

    --text-primary: #1f2937;
    --text-secondary: #6b7280;

    --primary: #2563eb;
    --primary-hover: #1d4ed8;
    --primary-soft: #eff6ff;

    --border: #e5e7eb;

    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;

    --shadow-sm: 0 1px 2px rgba(0,0,0,.04);
    --shadow-card: 0 4px 16px rgba(0,0,0,.04);
}
```

Do not over-engineer a design system, but keep styles maintainable.

---

# 37. JINJA COMPONENT REUSE

Reuse common patterns instead of duplicating HTML.

Examples:

* base layout
* navigation
* page header
* status badge
* alerts
* pagination
* empty state
* form errors

Use Jinja includes/macros where useful.

Do not duplicate sidebar markup across every page.

---

# 38. DO NOT CHANGE BUSINESS LOGIC

This redesign must NOT break:

* Login
* Logout
* Role permissions
* Database
* Repair creation
* Repair number generation
* Assignment
* Status workflow
* Upload
* Comments
* Search
* Filters
* Dashboard queries
* CSV
* PDF/Print
* Admin management

Do not change database values for visual reasons.

Keep internal values such as:

```text
pending
accepted
in_progress
completed

admin
teacher
technician

low
medium
high
```

Translate/display them through existing helpers.

---

# 39. TEST THE REAL USER FLOWS

After redesigning, run the application and manually verify these flows.

## Teacher

```text
Login
→ Dashboard
→ แจ้งซ่อมใหม่
→ Submit
→ ดูรายละเอียด
→ ติดตามสถานะ
→ Comment
```

## Admin

```text
Login
→ Dashboard
→ ดูงานใหม่
→ เปิดรายละเอียด
→ Assign Technician
→ ตรวจสอบสถานะ
→ User Management
```

## Technician

```text
Login
→ ดูงานที่ได้รับมอบหมาย
→ เปิดงาน
→ Start Repair
→ Comment
→ Upload After Image
→ Complete Repair
```

---

# 40. RESPONSIVE VERIFICATION

Inspect every important page at:

```text
375px
768px
1024px
1366px
```

Verify:

* no horizontal page overflow
* Thai text wraps correctly
* sidebar/navigation works
* cards fit properly
* forms remain usable
* tables adapt correctly
* buttons remain accessible
* upload UI works
* modal/dialog works
* repair detail remains easy to scan

Fix responsive problems before considering the redesign finished.

---

# 41. VISUAL CONSISTENCY

Every page must feel like the same application.

Keep consistent:

* Typography
* Colors
* Border radius
* Button style
* Input style
* Page header
* Card style
* Status badges
* Spacing
* Navigation

Do not redesign each page independently.

---

# 42. DESIGN PRIORITY

Use this priority:

1. Usability
2. Thai readability
3. Information hierarchy
4. Responsive behavior
5. Accessibility
6. Visual consistency
7. Soft/minimal aesthetics

Visual effects are the lowest priority.

---

# 43. FINAL QUALITY TARGET

The final application should feel like:

> A clean, friendly, modern internal school system that teachers and staff in Thailand can understand immediately without training.

It should NOT feel like:

> A generic Bootstrap admin template.

It should NOT feel like:

> An AI-generated futuristic dashboard.

It should NOT feel like:

> A complex enterprise management system.

---

# 44. IMPLEMENTATION PROCESS

Follow this process:

1. Read the complete existing project.
2. Read `PROJECT_SPEC.md`.
3. Inspect all Jinja templates.
4. Inspect all CSS.
5. Inspect JavaScript related to UI.
6. Identify reusable layouts/components.
7. Create/refine design tokens.
8. Redesign base layout.
9. Redesign navigation.
10. Redesign Login.
11. Redesign Dashboard.
12. Redesign Repair List.
13. Redesign Create Repair.
14. Redesign Repair Detail.
15. Redesign Admin Users.
16. Improve forms.
17. Improve empty states.
18. Improve mobile layouts.
19. Refactor duplicated CSS/HTML.
20. Run the application.
21. Test every role.
22. Test responsive layouts.
23. Run existing automated tests.
24. Fix any regressions.

Do not stop after changing only CSS variables or the dashboard.

Apply the design consistently across the entire application.

---

# 45. FINAL RESPONSE

When finished, provide a concise report containing:

* Files modified
* Main UI/UX improvements
* Responsive changes
* Components/styles reused
* Pages redesigned
* Thai UX improvements
* Functional flows tested
* Test results
* Any remaining UI limitations

Do not only provide recommendations.

Actually modify the current project and verify that the redesigned system still works.
