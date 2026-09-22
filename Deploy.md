Read the entire existing project before modifying anything.

Also read:

* `PROJECT_SPEC.md`
* `README.md`
* `.env.example`
* `requirements.txt`
* `app.py`
* `config.py`
* `extensions.py`
* all models
* all services
* all routes
* all templates
* tests

The application is an existing **School Repair Management System** built with Flask, Jinja2, SQLAlchemy, Flask-Login, SQLite, file uploads, SweetAlert2, CSV export, and optional PDF generation.

The application is already working locally.

Your task is to **prepare the entire project for deployment on Render** while preserving all existing functionality.

Do NOT rewrite the project from scratch.

Do NOT redesign the UI.

Do NOT change business logic unless necessary for production/deployment compatibility.

The final goal is:

> The project should be ready to push to GitHub and deploy on Render with minimal manual configuration.

---

# DEPLOYMENT TARGET

Target platform:

**Render Web Service**

Initial deployment architecture:

```text
GitHub Repository
        │
        ▼
Render Web Service
        │
        ├── Flask
        ├── Jinja2
        ├── SQLAlchemy
        ├── Flask-Login
        ├── Gunicorn
        │
        └── Persistent Disk
              ├── repair.db
              └── uploads/
```

For this deployment version, continue using:

* SQLite
* Render Persistent Disk
* Local uploaded images stored on the Persistent Disk

Do NOT migrate to PostgreSQL in this task unless the existing code absolutely requires it.

However, keep configuration flexible enough that `DATABASE_URL` could later point to PostgreSQL.

---

# 1. INSPECT PROJECT FIRST

Before changing code:

1. Inspect the complete repository.
2. Identify current app initialization.
3. Identify whether Flask uses `create_app()`.
4. Inspect current database initialization.
5. Inspect current SQLite path.
6. Inspect upload handling.
7. Inspect file serving logic.
8. Inspect `.env.example`.
9. Inspect `requirements.txt`.
10. Inspect tests.
11. Check whether Gunicorn already exists.
12. Check whether WeasyPrint is installed and how PDF fallback works.
13. Identify any code that assumes Windows/local filesystem paths.

Create an internal checklist of changes.

Then implement them.

Do not modify files unnecessarily.

---

# 2. PRODUCTION SERVER

The application must not use the Flask development server in production.

Add and configure:

```text
gunicorn
```

Update `requirements.txt` if necessary.

The Render Start Command should support the current Flask architecture.

If the application uses an application factory:

```python
def create_app():
    ...
```

the preferred command should be compatible with:

```bash
gunicorn "app:create_app()" --bind 0.0.0.0:$PORT
```

If the project exposes:

```python
app = create_app()
```

then use:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

Inspect the existing project and choose the correct approach.

Do not create two competing app initialization patterns.

---

# 3. PYTHON VERSION

Add a `.python-version` file.

Use a stable production Python version compatible with the existing dependencies.

Prefer:

```text
3.12
```

unless the project dependencies require a different supported version.

Do not use an unnecessarily new Python version that could break dependencies.

Make sure the chosen version matches the project's requirements.

---

# 4. REQUIREMENTS.TXT

Review `requirements.txt`.

Ensure it contains all packages actually required by production.

At minimum verify packages such as:

```text
Flask
Flask-SQLAlchemy
Flask-Login
Flask-WTF
Werkzeug
python-dotenv
gunicorn
```

Include Flask-Migrate only if the project actually uses it.

Include WeasyPrint only if the existing PDF implementation requires it and installation is viable.

Remove unused dependencies if clearly safe.

Do not remove packages required by tests or application runtime accidentally.

---

# 5. PRODUCTION CONFIGURATION

Refactor `config.py` where necessary so configuration comes from environment variables.

Support at minimum:

```text
SECRET_KEY
DATABASE_URL
UPLOAD_FOLDER
MAX_CONTENT_LENGTH
```

Example concept:

```python
import os
from pathlib import Path


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///repair.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        str(Path("static") / "uploads")
    )

    MAX_CONTENT_LENGTH = int(
        os.getenv(
            "MAX_CONTENT_LENGTH",
            5 * 1024 * 1024
        )
    )
```

Adapt this to the existing architecture.

Do not blindly copy it if current config structure differs.

---

# 6. SECRET KEY SAFETY

Production must not use a hardcoded development SECRET_KEY.

Requirements:

* Read `SECRET_KEY` from environment.
* Development may use a safe fallback only if needed.
* Production should fail clearly or warn if SECRET_KEY is missing.
* `.env` must never be committed.

Update `.env.example` with a placeholder only:

```env
SECRET_KEY=change-me
```

Do not include an actual production secret.

---

# 7. SQLITE + RENDER PERSISTENT DISK

Prepare the project so SQLite can live on Render Persistent Disk.

Production example:

```text
/opt/render/project/src/storage/repair.db
```

Expected environment variable:

```env
DATABASE_URL=sqlite:////opt/render/project/src/storage/repair.db
```

Do not hardcode this production value into application source code.

The application should still work locally with a normal SQLite path.

The same codebase must support:

```text
Local:
sqlite:///repair.db

Render:
sqlite:////opt/render/project/src/storage/repair.db
```

---

# 8. UPLOAD STORAGE

Current uploaded files must also support Render Persistent Disk.

Production upload folder:

```text
/opt/render/project/src/storage/uploads
```

Expected environment:

```env
UPLOAD_FOLDER=/opt/render/project/src/storage/uploads
```

Local development should continue to support:

```text
static/uploads
```

or the existing local upload directory.

Do not hardcode the production upload path.

---

# 9. IMPORTANT: FILE SERVING

Because production uploads may live outside Flask's `/static` directory, inspect how images are currently displayed.

If templates currently assume:

```python
url_for("static", filename=image.image_path)
```

this may no longer work when `UPLOAD_FOLDER` is outside `static/`.

Fix this cleanly.

Recommended approach:

Create a secure authenticated route for serving uploaded repair images, for example conceptually:

```text
/uploads/<filename>
```

or:

```text
/repair-images/<path:filename>
```

Requirements:

* Read files from configured `UPLOAD_FOLDER`.
* Prevent directory traversal.
* Only serve valid files.
* Respect existing repair authorization where practical.
* Do not expose arbitrary filesystem paths.
* Continue working locally and on Render.

Use Flask helpers such as `send_from_directory()` where appropriate.

Update templates to use the new route instead of assuming uploads are inside `/static`.

Do not weaken existing access control.

---

# 10. CREATE STORAGE DIRECTORIES SAFELY

At application startup, ensure required directories exist.

For example:

```text
UPLOAD_FOLDER
database parent directory
```

Use safe directory creation such as:

```python
Path(...).mkdir(parents=True, exist_ok=True)
```

Do not crash merely because the upload directory does not yet exist.

However, do not silently create arbitrary invalid filesystem paths.

---

# 11. DATABASE INITIALIZATION

Inspect the current:

```bash
flask --app app init-db
```

behavior.

The current project may create demo accounts during initialization.

Prepare database initialization so deployment is safe and **idempotent**.

Requirements:

* Running initialization more than once must NOT delete existing data.
* Do not drop tables.
* Do not recreate/reset the production database.
* Existing repair requests must remain intact.
* Existing users must remain intact.

If necessary, separate commands into:

```bash
flask --app app init-db
```

and:

```bash
flask --app app seed-demo
```

Recommended behavior:

### init-db

Only:

```text
create missing tables
perform safe initialization
```

### seed-demo

Only:

```text
create development/demo users if they do not already exist
```

Do not automatically seed demo accounts in production unless explicitly configured.

---

# 12. DO NOT INITIALIZE PERSISTENT DATABASE DURING BUILD

Do NOT rely on the Render Build Command to initialize the SQLite database on Persistent Disk.

Build Command should preferably remain:

```bash
pip install -r requirements.txt
```

Do not use:

```bash
pip install -r requirements.txt &&
flask init-db
```

for persistent production storage.

Instead create a safe runtime startup mechanism.

---

# 13. STARTUP SCRIPT

Create a clean production startup script if useful.

For example:

```text
start.sh
```

Concept:

```bash
#!/usr/bin/env bash
set -e

python -m flask --app app init-db
exec gunicorn "app:create_app()" --bind 0.0.0.0:${PORT:-10000}
```

Only use this pattern if `init-db` has been made fully idempotent and production-safe.

Otherwise use another safe mechanism.

Make sure shell scripts use Unix line endings.

Make executable instructions clear in README.

Do not reset or reseed database contents during every restart.

---

# 14. RENDER.YAML

Create a `render.yaml` Blueprint configuration if practical.

It should describe the web service configuration without exposing secrets.

Example concept:

```yaml
services:
  - type: web
    name: school-repair-system
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: ./start.sh
```

Add appropriate persistent disk configuration if supported by the current Render Blueprint format.

Do NOT place:

```text
SECRET_KEY
passwords
private tokens
```

inside `render.yaml`.

For secret variables, define keys without exposing their values or document that they must be entered in Render Dashboard.

If `render.yaml` would create unnecessary complexity for the current project, still prepare it in a simple and valid form.

---

# 15. .ENV.EXAMPLE

Update `.env.example` to clearly support both local and Render configuration.

Example:

```env
SECRET_KEY=change-me

DATABASE_URL=sqlite:///repair.db

UPLOAD_FOLDER=static/uploads

MAX_CONTENT_LENGTH=5242880
```

Add comments if useful.

Do not put Render-specific production secrets into this file.

---

# 16. .GITIGNORE

Review `.gitignore`.

Ensure it excludes:

```gitignore
.env
.venv/
venv/

__pycache__/
*.pyc

*.db

storage/

static/uploads/*

.pytest_cache/
.coverage

.DS_Store
```

Preserve placeholder files such as `.gitkeep` if required.

Do not accidentally ignore source code or migrations.

---

# 17. PRODUCTION DEBUG MODE

Ensure production does NOT run with:

```text
DEBUG=True
```

or:

```bash
flask run --debug
```

Production must run through Gunicorn.

Development mode must still be easy to use locally.

---

# 18. HOST / PORT

Ensure the production server listens on:

```text
0.0.0.0
```

and uses Render's:

```text
$PORT
```

Do not hardcode port `5000` for production.

Local Flask development can continue using port 5000.

---

# 19. DATABASE URL COMPATIBILITY

Keep SQLAlchemy configuration flexible.

If later `DATABASE_URL` uses:

```text
postgresql://...
```

the project should not require major architecture changes.

Avoid SQLite-specific assumptions in general application configuration where unnecessary.

Do NOT migrate to PostgreSQL now.

---

# 20. REQUEST NUMBER SAFETY

Current repair numbers use:

```text
RP-YYYYMM-XXX
```

Review the implementation for deployment.

Since the initial Render deployment uses one instance + SQLite, the current mechanism can remain.

However:

* ensure request number has a UNIQUE database constraint
* handle collisions safely
* do not generate the running number purely from untrusted request data
* preserve current business rules

Do not unnecessarily redesign the numbering system.

---

# 21. UPLOAD SECURITY

Preserve or improve existing upload protections.

Must retain:

* allowed extensions
* MIME/content checking if currently available
* file signature checking if currently available
* UUID filenames
* `secure_filename`
* file size limit
* path traversal protection

Never save uploaded files using raw user-provided filenames.

Make sure upload handling still works when `UPLOAD_FOLDER` is an absolute Render filesystem path.

---

# 22. CSRF

Verify that all state-changing HTML forms remain protected by CSRF.

This includes:

* login if applicable
* logout
* create repair
* assign technician
* start repair
* complete repair
* comments
* user creation
* user editing
* password reset
* account disable/delete

Do not disable CSRF just to make deployment easier.

---

# 23. SESSION / COOKIES

Review Flask session configuration for production.

Use safe settings where practical.

For production HTTPS, consider:

```python
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
```

If appropriate for Render HTTPS deployment:

```python
SESSION_COOKIE_SECURE = True
```

Make environment-sensitive choices so localhost development remains usable.

Do not break login locally.

---

# 24. PROXY / HTTPS HANDLING

Render terminates HTTPS before forwarding traffic to the Flask service.

Inspect whether the application needs ProxyFix for correct scheme/host handling.

If required, configure carefully using Werkzeug:

```python
ProxyFix
```

Do not add incorrect proxy counts blindly.

Only apply if needed by URL generation, secure cookies, or scheme detection.

---

# 25. ERROR HANDLING

Ensure production has user-friendly handlers for:

```text
400
403
404
413
500
```

Important:

`413 Payload Too Large`

should show a Thai message explaining that the uploaded file is too large.

Do not expose Python traceback or sensitive internal information to end users.

Log server-side exceptions appropriately.

---

# 26. HEALTH CHECK

Add a lightweight health route if one does not exist.

Example:

```text
/health
```

Response:

```json
{
  "status": "ok"
}
```

It should NOT expose:

* database credentials
* SECRET_KEY
* filesystem paths
* user information

Use it for Render health checking if useful.

---

# 27. PDF / WEASYPRINT

Inspect the existing PDF feature.

The application already has browser print fallback.

Requirements:

* Do not let WeasyPrint failure break the whole application.
* Keep Browser Print / Save as PDF working.
* Gracefully handle environments where WeasyPrint native libraries are unavailable.
* Do not block deployment because PDF library is optional.

If WeasyPrint creates deployment instability, document it as optional and preserve print fallback.

Do not remove existing PDF functionality without a reason.

---

# 28. STATIC FILES

Verify that CSS, JavaScript, images, favicon, and any font assets load correctly behind Gunicorn on Render.

Do not use absolute localhost URLs such as:

```text
http://127.0.0.1:5000
```

inside templates.

Use:

```python
url_for(...)
```

where appropriate.

---

# 29. THAI UI

Preserve the Thai-first UI.

Verify UTF-8 remains correct in production.

Keep:

```html
<meta charset="UTF-8">
<html lang="th">
```

Thai text must not become garbled after deployment.

Do not change internal enum/database values into Thai.

---

# 30. TESTING

Before finishing, run the existing test suite:

```bash
python -m pytest -q
```

Current project previously had tests covering:

* Login
* Logout
* Authorization
* Repair creation
* Request numbers
* Validation
* Workflow
* Uploads
* Demo flow
* Thai localization

Make sure existing tests still pass.

Add new tests where useful for deployment-specific changes, particularly:

* configured upload directory
* image-serving route
* idempotent database initialization
* production config
* health route
* authorization for uploaded files if implemented

Do not weaken tests to make them pass.

Fix the implementation.

---

# 31. TEST GUNICORN LOCALLY

After code changes, verify the production server command locally.

For example:

```bash
gunicorn "app:create_app()" --bind 127.0.0.1:8000
```

or the correct command for the project's actual structure.

Verify:

* application starts
* login page loads
* static assets load
* authentication works
* uploaded images work
* database works
* no import errors occur

---

# 32. TEST COMPLETE USER FLOW

Verify at least this full workflow:

```text
Teacher login
→ Create repair
→ Upload before image

Admin login
→ See repair
→ Assign technician
→ Set due date

Technician login
→ See assigned task
→ Start repair
→ Add result
→ Add cost
→ Upload after image
→ Complete repair

Teacher login
→ View completed repair
```

Also test:

```text
CSV Export
Print page
PDF fallback
Comments
Admin User Management
```

---

# 33. DEMO ACCOUNTS

Current development demo accounts may include:

```text
admin
teacher01
tech01
```

Keep demo seeding available for development and classroom presentation.

But:

* Do not force-create them on every production start.
* Do not reset their passwords automatically.
* Clearly label them as demo-only.
* Document how to seed them manually.

---

# 34. README DEPLOYMENT DOCUMENTATION

Update `README.md` with a new section:

```text
Deploy on Render
```

Include:

## Prerequisites

```text
GitHub repository
Render account
```

## Render Service

```text
Service Type:
Web Service

Runtime:
Python

Build Command:
pip install -r requirements.txt

Start Command:
<actual final production command>
```

## Environment Variables

Document:

```text
SECRET_KEY
DATABASE_URL
UPLOAD_FOLDER
MAX_CONTENT_LENGTH
```

Example production values may show paths but NEVER show a real secret.

## Persistent Disk

Document recommended mount path:

```text
/opt/render/project/src/storage
```

Database:

```text
/opt/render/project/src/storage/repair.db
```

Uploads:

```text
/opt/render/project/src/storage/uploads
```

## First Deployment

Explain how database initialization happens.

## Demo Seed

Explain how demo users can be seeded if required.

## Troubleshooting

Include common issues such as:

```text
Gunicorn import error
database directory missing
uploads not displaying
WeasyPrint unavailable
SECRET_KEY missing
SQLite permission/path error
```

README instructions must match the actual implementation.

---

# 35. OPTIONAL DEPLOYMENT CHECKLIST

Add a small checklist to README:

```text
[ ] Tests pass
[ ] SECRET_KEY configured
[ ] Persistent Disk attached
[ ] DATABASE_URL configured
[ ] UPLOAD_FOLDER configured
[ ] Debug disabled
[ ] Gunicorn starts
[ ] Database initialized
[ ] Login works
[ ] Upload works
[ ] Full repair workflow works
```

---

# 36. SECURITY CHECK

Before finishing, review for accidental secrets.

Search repository for:

```text
SECRET_KEY
password
token
API_KEY
localhost credentials
```

Ensure no real secret values are committed.

Do not delete legitimate test fixture passwords unless needed.

Make sure demo credentials are clearly identified as development/demo credentials only.

---

# 37. DO NOT BREAK CURRENT ARCHITECTURE

Preserve existing:

```text
Application Factory
Routes
Services
Models
Enums
Localization
Templates
Role authorization
Repair workflow
```

Do not flatten the architecture into one `app.py`.

Do not move business logic back into routes.

Keep OOAD/OOP structure intact.

---

# 38. EXPECTED FILES AFTER PREPARATION

The project should have something similar to:

```text
Repair-Request-System/
│
├── app.py
├── config.py
├── extensions.py
├── localization.py
│
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── .python-version
├── render.yaml
├── start.sh
│
├── enums/
├── models/
├── routes/
├── services/
├── templates/
├── static/
├── tests/
│
└── storage/
    └── .gitkeep
```

Adjust according to the actual project.

Do not create meaningless placeholder files if they are unnecessary.

---

# 39. RENDER CONFIGURATION TARGET

The final project should be deployable with settings approximately equivalent to:

```text
Service:
Web Service

Runtime:
Python

Build Command:
pip install -r requirements.txt

Start Command:
./start.sh
```

or the correct direct Gunicorn command if no startup script is needed.

Persistent Disk:

```text
Mount Path:
/opt/render/project/src/storage
```

Environment variables:

```text
SECRET_KEY=<set in Render dashboard>

DATABASE_URL=
sqlite:////opt/render/project/src/storage/repair.db

UPLOAD_FOLDER=
/opt/render/project/src/storage/uploads

MAX_CONTENT_LENGTH=
5242880
```

Do not hardcode these production values into source code.

---

# 40. FINAL VERIFICATION

Before declaring the task complete:

1. Install dependencies.
2. Run pytest.
3. Verify all tests pass.
4. Run Gunicorn locally.
5. Check `/health`.
6. Login as Teacher.
7. Create repair.
8. Verify database write.
9. Upload image.
10. Verify image loads.
11. Login as Admin.
12. Assign technician.
13. Login as Technician.
14. Start and complete repair.
15. Verify final status.
16. Test CSV.
17. Test print/PDF fallback.
18. Check no debug mode.
19. Check no secrets are committed.
20. Confirm README deployment instructions are accurate.
21. Inspect `git diff`.
22. Fix any deployment blockers found.

Do not stop after merely adding `render.yaml`.

The entire application must be genuinely prepared for production-style Render deployment.

---

# 41. FINAL RESPONSE FORMAT

When finished, report:

## Deployment preparation completed

### Files created

List them.

### Files modified

List them.

### Production changes

Summarize:

* Gunicorn
* Python version
* Environment config
* Persistent SQLite path
* Upload path
* Upload serving
* Safe database initialization
* Render config
* Security changes

### Render settings

Provide the exact final:

```text
Build Command
Start Command
Persistent Disk Mount Path
Environment Variables
```

based on the implementation you actually created.

### Test results

Report:

```text
pytest result
Gunicorn startup result
```

### Manual flow verification

Report which flows were tested.

### Remaining limitations

Mention only real remaining limitations.

Do not only explain what should be changed.

Actually modify and verify the current project so it is ready to push to GitHub and deploy on Render.
