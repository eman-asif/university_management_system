from django.urls import path
from .views import *

urlpatterns = [
    path('students-per-department/', StudentsPerDepartmentView.as_view()),
    path('faculty-per-department/', FacultyPerDepartmentView.as_view()),
    path('enrollment-per-program/', EnrollmentPerProgramView.as_view()),
    path('attendance-distribution/', AttendanceDistributionView.as_view()),
    path('grades-distribution/', GradesDistributionView.as_view()),
    path('withdrawals-per-course/', WithdrawalsPerCourseView.as_view()),
    path('top-performing-students/', TopPerformingStudentsView.as_view()),
    path('low-attendance-students/', LowAttendanceStudentsView.as_view()),
    path('popular-courses/', PopularCoursesView.as_view()),
    path('top-students/program/<int:program_id>/', TopStudentsByDepartmentView.as_view(), name='top_students_by_department'),
    path('faculty-teaching-load/', FacultyTeachingLoadView.as_view()),
    path('average-grades/department/', AverageGradesByDepartmentView.as_view()),
    path('withdrawal-rate/department/', WithdrawalRateByDepartmentView.as_view()),
    path('attendance-summary/department/', AttendanceSummaryByDepartmentView.as_view()),
    path('enrollment-trends/program/', EnrollmentTrendsByProgramView.as_view()),
    path('top-courses/program/<int:program_id>/', TopCoursesByProgramView.as_view()),
    path('low-performing-students/program/<int:program_id>/', LowPerformingStudentsByProgramView.as_view()),
    path('programs/students/', StudentsPerProgramView.as_view(), name='students-per-program'),
    path('programs/faculty/', FacultyPerProgramView.as_view(), name='faculty-per-program'),
    path('programs/grades/average/', AverageGradesByProgramView.as_view(), name='average-grades-by-program'),
    path('programs/withdrawals/', WithdrawalRateByProgramView.as_view(), name='withdrawals-by-program'),
    path('programs/attendance/', AttendanceSummaryByProgramView.as_view(), name='attendance-by-program'),
    path('programs/<int:program_id>/top-students/', TopStudentsByProgramView.as_view(), name='top-students-by-program'),


]
