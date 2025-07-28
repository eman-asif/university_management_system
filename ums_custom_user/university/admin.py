from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('user_type',)}),
    )
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Enrollment)
admin.site.register(Withdrawal)
admin.site.register(Grade)
admin.site.register(Attendance)
admin.site.register(Timetable)
