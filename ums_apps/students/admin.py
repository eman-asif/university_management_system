from django.contrib import admin
from .models import Student, Enrollment, Withdrawal, Grade, Attendance

admin.site.register(Student)
admin.site.register(Enrollment)
admin.site.register(Withdrawal)
admin.site.register(Grade)
admin.site.register(Attendance)
