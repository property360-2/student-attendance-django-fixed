# [students/views.py]
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Student
from .forms import StudentForm

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        # Only show students owned by the logged-in user
        return Student.objects.filter(owner=self.request.user)

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')

    def form_valid(self, form):
        # Attach the logged-in user as the owner of the new student
        form.instance.owner = self.request.user
        return super().form_valid(form)

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')

    def get_queryset(self):
        # Users can only edit their own students
        return Student.objects.filter(owner=self.request.user)

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:list')

    def get_queryset(self):
        # Users can only delete their own students
        return Student.objects.filter(owner=self.request.user)
