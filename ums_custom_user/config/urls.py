"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from university.views import (
    DepartmentViewSet, ProgramViewSet, CourseViewSet,
    StudentViewSet, FacultyViewSet, EnrollmentViewSet,
    WithdrawalViewSet, GradeViewSet, AttendanceViewSet,
    TimetableViewSet,
    StudentGPAView, CourseWithdrawalsView, AttendanceSummaryView
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'programs', ProgramViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'students', StudentViewSet)
router.register(r'faculty', FacultyViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'withdrawals', WithdrawalViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'timetables', TimetableViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('stats/student-gpa/', StudentGPAView.as_view(), name='student-gpa'),
    path('stats/course-withdrawals/', CourseWithdrawalsView.as_view(), name='course-withdrawals'),
    path('stats/attendance-summary/', AttendanceSummaryView.as_view(), name='attendance-summary'),
]