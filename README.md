# [README.md]
# AttendLite — Student Attendance (Django + Atomic Templates) — FIXED

Fixed version with:
- Default Django auth user (no custom user model, no AUTH_USER_MODEL override)
- Proper templatetags in `core/templatetags/extras.py` and `{% load extras %}` in templates
- Clean migrations path; start fresh DB if you had a prior custom user

## Folder Structure
(see repository tree)

## How to Run

### 1) Create environment & install (choose one)

**Bash (Linux/macOS):**
```bash
cd student_attendance
python3 -m venv .venv
source .venv/bin/activate
pip install "Django>=4.2,<6.0"
```

**PowerShell (Windows):**
```powershell
cd student_attendance
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "Django>=4.2,<6.0"
```

**CMD (Windows):**
```bat
cd student_attendance
py -m venv .venv
.\.venv\Scripts\activate.bat
pip install "Django>=4.2,<6.0"
```

### 2) Initialize DB
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 3) Run
```bash
python manage.py runserver
```

## Notes
- If you previously ran migrations with a custom user model, delete `db.sqlite3` and re-run migrations.
- Timezone is set to `Asia/Manila`.
- Atomic components live in `templates/components` with atoms/molecules/organisms.
