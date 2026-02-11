# [students/forms.py]
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'student_id', 'class_section', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'input', 'placeholder':'First name'}),
            'last_name': forms.TextInput(attrs={'class':'input', 'placeholder':'Last name'}),
            'email': forms.EmailInput(attrs={'class':'input', 'placeholder':'Email'}),
            'student_id': forms.TextInput(attrs={'class':'input', 'placeholder':'Student ID'}),
            'class_section': forms.TextInput(attrs={'class':'input', 'placeholder':'Class/Section (e.g. BSIT 2A)'}),
            'is_active': forms.CheckboxInput(attrs={'class':'checkbox'}),
        }
