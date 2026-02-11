# [attendance/forms.py]
from django import forms

class DateSelectForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'input'}))

class AttendanceLineForm(forms.Form):
    student_id = forms.IntegerField(widget=forms.HiddenInput())
    status = forms.ChoiceField(
        choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')],
        widget=forms.Select(attrs={'class': 'select'}),
    )
    remarks = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Remarks (optional)'}),
    )
    late_reason = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'input', 'placeholder': 'Late reason (optional, if status is Late)'}
        ),
    )
