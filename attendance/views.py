# [attendance/views.py]
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.contrib import messages
from django.utils import timezone

from .models import AttendanceRecord
from .forms import DateSelectForm, AttendanceLineForm
from students.models import Student


@login_required
def attendance_list(request):
    date_str = request.GET.get('date')
    student_id = request.GET.get('student')
    # Only show attendance records created by the logged-in user
    qs = AttendanceRecord.objects.filter(created_by=request.user)
    selected_date = None
    selected_student = None
    
    if date_str:
        try:
            selected_date = timezone.datetime.fromisoformat(date_str).date()
        except Exception:
            selected_date = None
        if selected_date:
            qs = qs.filter(date=selected_date)
    
    if student_id:
        try:
            from students.models import Student
            # Ensure the selected student also belongs to the current user
            selected_student = Student.objects.get(id=student_id, owner=request.user)
            qs = qs.filter(student=selected_student)
        except:
            pass
    
    qs = qs.select_related('student').order_by('-date', 'student__last_name')
    return render(
        request,
        'attendance/attendance_list.html',
        {
            'records': qs,
            'selected_date': selected_date,
            'selected_student': selected_student,
        },
    )


@login_required
def attendance_mark(request):
    # Only list active students owned by the logged-in user
    students = list(
        Student.objects.filter(is_active=True, owner=request.user).order_by('last_name', 'first_name')
    )
    num_students = len(students)
    # Use min_num/max_num to ensure formset has correct number of forms
    if num_students > 0:
        FormSet = formset_factory(AttendanceLineForm, extra=0, min_num=num_students, max_num=num_students)
    else:
        FormSet = formset_factory(AttendanceLineForm, extra=0)

    if request.method == 'GET':
        form = DateSelectForm(request.GET or None)
        if form.is_valid():
            date = form.cleaned_data['date']
        else:
            date = timezone.localdate()
            form = DateSelectForm(initial={'date': date})

        existing = {
            r.student_id: r
            for r in AttendanceRecord.objects.filter(
                date=date,
                created_by=request.user,
            ).select_related('student')
        }
        initial = []
        for s in students:
            record = existing.get(s.id)
            initial.append(
                {
                    'student_id': s.id,
                    'status': getattr(record, 'status', 'present'),
                    'remarks': getattr(record, 'remarks', ''),
                }
            )

        formset = FormSet(initial=initial)
        rows = list(zip(students, formset.forms))
        return render(
            request,
            'attendance/attendance_mark.html',
            {
                'date_form': form,
                'formset': formset,
                'rows': rows,
                'date': date,
            },
        )

    # POST -> save
    form = DateSelectForm(request.POST)
    
    # Get date first, even if form is invalid, to determine number of students
    try:
        date_str = request.POST.get('date')
        if date_str:
            from datetime import datetime
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = timezone.localdate()
    except:
        date = timezone.localdate()

    # Prevent recording attendance in the future (for realism)
    future_date = False
    if date > timezone.localdate():
        future_date = True
        messages.error(request, "You cannot record attendance for a future date.")
    # Create formset with POST data
    formset = FormSet(request.POST)
    
    if form.is_valid() and formset.is_valid() and not future_date:
        date = form.cleaned_data['date']
        count = 0
        for f in formset:
            cd = f.cleaned_data
            sid = cd.get('student_id')
            if sid:
                status = cd.get('status', 'present')
                remarks = cd.get('remarks', '')
                late_reason = cd.get('late_reason', '')
                AttendanceRecord.objects.update_or_create(
                    student_id=sid,
                    date=date,
                    defaults={
                        'status': status,
                        'remarks': remarks,
                        'late_reason': late_reason if status == 'late' else '',
                        'created_by': request.user,
                    },
                )
                count += 1
        messages.success(request, f"Saved {count} attendance rows for {date}.")
        return redirect('attendance:list')

    # Show errors - rebuild formset for display with existing data
    existing = {
        r.student_id: r
        for r in AttendanceRecord.objects.filter(
            date=date,
            created_by=request.user,
        ).select_related('student')
    }
    initial = []
    for s in students:
        record = existing.get(s.id)
        initial.append({
            'student_id': s.id,
            'status': getattr(record, 'status', 'present'),
            'remarks': getattr(record, 'remarks', ''),
            'late_reason': getattr(record, 'late_reason', ''),
        })
    # Recreate formset with POST data for error display
    formset = FormSet(request.POST, initial=initial)
    
    messages.error(request, "Please correct the errors below.")
    rows = list(zip(students, formset.forms))
    return render(
        request,
        'attendance/attendance_mark.html',
        {
            'date_form': form,
            'formset': formset,
            'rows': rows,
            'date': date,
        },
    )
