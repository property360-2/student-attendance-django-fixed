# [attendance/admin.py]
from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('date','student','status','remarks','created_by','created_at')
    list_filter = ('date','status')
    search_fields = ('student__first_name','student__last_name','student__student_id','remarks')
