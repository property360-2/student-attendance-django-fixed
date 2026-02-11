# [student_attendance/asgi.py]
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_attendance.settings')
application = get_asgi_application()
