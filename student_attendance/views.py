# [student_attendance/views.py]
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from collections import Counter, defaultdict
from datetime import timedelta
from calendar import month_name
from students.models import Student
from attendance.models import AttendanceRecord

@login_required
def dashboard(request):
    today = timezone.localdate()
    # Only count students owned by the logged-in user
    total_students = Student.objects.filter(is_active=True, owner=request.user).count()
    
    # Get search query
    search_query = request.GET.get('search', '').strip()
    
    # Overall stats (all dates) for this user only
    user_records = AttendanceRecord.objects.filter(created_by=request.user)
    overall_present = user_records.filter(status='present').count()
    overall_absent = user_records.filter(status='absent').count()
    overall_late = user_records.filter(status='late').count()
    
    # Today's stats for this user
    today_present = user_records.filter(date=today, status='present').count()
    today_absent = user_records.filter(date=today, status='absent').count()
    today_late = user_records.filter(date=today, status='late').count()
    
    # Get all unique dates with attendance records and their counts
    dates_with_stats = []
    unique_dates = user_records.values_list('date', flat=True).distinct().order_by('-date')
    
    for date in unique_dates:
        date_present = user_records.filter(date=date, status='present').count()
        date_absent = user_records.filter(date=date, status='absent').count()
        date_late = user_records.filter(date=date, status='late').count()

        dates_with_stats.append(
            {
                'date': date,
                'present': date_present,
                'absent': date_absent,
                'late': date_late,
                'total': date_present + date_absent + date_late,
            }
        )

    # Weekly and monthly summaries (for tables and charts)
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    start_of_month = today.replace(day=1)

    week_records = user_records.filter(date__gte=start_of_week, date__lte=today)
    month_records = user_records.filter(date__gte=start_of_month, date__lte=today)

    def summarize(records_qs):
        return {
            'present': records_qs.filter(status='present').count(),
            'absent': records_qs.filter(status='absent').count(),
            'late': records_qs.filter(status='late').count(),
            'total': records_qs.count(),
        }

    weekly_summary = summarize(week_records)
    monthly_summary = summarize(month_records)

    # Group attendance data by month for separate charts
    monthly_charts = defaultdict(lambda: {'labels': [], 'present': [], 'absent': [], 'late': []})
    
    for date_stat in dates_with_stats:
        date = date_stat['date']
        month_key = f"{date.year}-{date.month:02d}"  # e.g., "2024-01"
        month_label = f"{month_name[date.month]} {date.year}"  # e.g., "January 2024"
        
        monthly_charts[month_key]['month_label'] = month_label
        monthly_charts[month_key]['labels'].append(date.isoformat())
        monthly_charts[month_key]['present'].append(date_stat['present'])
        monthly_charts[month_key]['absent'].append(date_stat['absent'])
        monthly_charts[month_key]['late'].append(date_stat['late'])
    
    # Convert to list sorted by month (oldest first)
    charts_by_month = []
    for month_key in sorted(monthly_charts.keys()):
        charts_by_month.append({
            'month_key': month_key,
            'month_label': monthly_charts[month_key]['month_label'],
            'labels': monthly_charts[month_key]['labels'],
            'present': monthly_charts[month_key]['present'],
            'absent': monthly_charts[month_key]['absent'],
            'late': monthly_charts[month_key]['late'],
        })
    
    chart_data = {
        'charts_by_month': charts_by_month,
        'weekly': weekly_summary,
        'monthly': monthly_summary,
        'today': today.isoformat(),
        'start_of_week': start_of_week.isoformat(),
        'start_of_month': start_of_month.isoformat(),
    }

    # Calculate student-level statistics with ranking based on points
    students_with_stats = []
    students = Student.objects.filter(is_active=True, owner=request.user)
    
    # Apply search filter
    if search_query:
        students = students.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(student_id__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    students = students.order_by('last_name', 'first_name')
    
    for student in students:
        records = user_records.filter(student=student)
        total_records = records.count()

        if total_records > 0:
            present_count = records.filter(status='present').count()
            absent_count = records.filter(status='absent').count()
            late_count = records.filter(status='late').count()

            # Calculate percentages
            present_pct = round((present_count / total_records) * 100, 1)
            absent_pct = round((absent_count / total_records) * 100, 1)
            late_pct = round((late_count / total_records) * 100, 1)

            # Attendance points: Present=1, Late=0.5, Absent=0
            points = present_count * 1.0 + late_count * 0.5

            # Determine most common status
            status_counts = Counter(records.values_list('status', flat=True))
            most_common_status = status_counts.most_common(1)[0][0] if status_counts else None
            most_common_count = status_counts.most_common(1)[0][1] if status_counts else 0

            # Perfect attendance = no absent or late
            is_perfect = absent_count == 0 and late_count == 0

            # Frequently late (simple rule: at least 3 times or 20% of records)
            is_late_risk = late_count >= 3 or (total_records > 0 and late_pct >= 20)

            students_with_stats.append(
                {
                    'student': student,
                    'total_records': total_records,
                    'present_count': present_count,
                    'absent_count': absent_count,
                    'late_count': late_count,
                    'present_pct': present_pct,
                    'absent_pct': absent_pct,
                    'late_pct': late_pct,
                    'most_common_status': most_common_status,
                    'most_common_count': most_common_count,
                    'points': points,
                    'is_perfect': is_perfect,
                    'is_late_risk': is_late_risk,
                }
            )
        else:
            # Student with no attendance records (no points / no rank)
            students_with_stats.append(
                {
                    'student': student,
                    'total_records': 0,
                    'present_count': 0,
                    'absent_count': 0,
                    'late_count': 0,
                    'present_pct': 0,
                    'absent_pct': 0,
                    'late_pct': 0,
                    'most_common_status': None,
                    'most_common_count': 0,
                    'points': 0.0,
                    'is_perfect': False,
                    'is_late_risk': False,
                }
            )

    # Sort by points (highest first), then by present count and name
    students_with_stats.sort(
        key=lambda x: (
            x['points'],
            x['present_count'],
            x['student'].last_name,
            x['student'].first_name,
        ),
        reverse=True,
    )

    # Assign ranks with ties: students with same points share same rank
    current_rank = 0
    previous_points = None
    for stat in students_with_stats:
        if stat['total_records'] == 0:
            stat['rank'] = None
            continue
        if previous_points is None or stat['points'] != previous_points:
            current_rank += 1
            previous_points = stat['points']
        stat['rank'] = current_rank

    context = {
        'today': today,
        'total_students': total_students,
        'present': overall_present,
        'absent': overall_absent,
        'late': overall_late,
        'today_present': today_present,
        'today_absent': today_absent,
        'today_late': today_late,
        'dates_with_stats': dates_with_stats,
        'students_with_stats': students_with_stats,
        'search_query': search_query,
        'weekly_summary': weekly_summary,
        'monthly_summary': monthly_summary,
        'chart_data': chart_data,
    }
    return render(request, 'dashboard.html', context)
