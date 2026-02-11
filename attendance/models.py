# [attendance/models.py]
from django.db import models
from django.conf import settings
from students.models import Student


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_records',
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    remarks = models.CharField(max_length=255, blank=True)
    late_reason = models.CharField(
        max_length=255,
        blank=True,
        help_text='Optional reason if the student is late.',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date', 'student__last_name']

    def __str__(self):
        return f"{self.date} - {self.student} - {self.status}"

    @property
    def points(self) -> float:
        """Attendance points: Present = 1, Late = 0.5, Absent = 0"""
        if self.status == 'present':
            return 1.0
        if self.status == 'late':
            return 0.5
        return 0.0
