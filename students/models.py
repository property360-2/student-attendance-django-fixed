# [students/models.py]
from django.db import models
from django.conf import settings


class Student(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='students',
        help_text='User account that owns this student record',
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    student_id = models.CharField(max_length=30)
    class_section = models.CharField(
        max_length=50,
        blank=True,
        help_text='Class or section (e.g. BSIT 2A)',
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'student_id'],
                name='unique_student_id_per_owner',
            ),
            models.UniqueConstraint(
                fields=['owner', 'email'],
                name='unique_email_per_owner',
            ),
        ]

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.student_id})"
