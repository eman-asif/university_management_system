from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle
from django.db.models import Count, Avg

from students.models import Student, Enrollment, Withdrawal, Attendance, Grade
from faculty.models import Faculty
from academics.models import Department, Program, Course

from accounts.throttling import AdminThrottle
# 1. Count of Students in Each Department
class StudentsPerDepartmentView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Student.objects.values('department__name').annotate(total=Count('id'))
        return Response(data)

# 2. Count of Faculty in Each Department
class FacultyPerDepartmentView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Faculty.objects.values('department__name').annotate(total=Count('id'))
        return Response(data)

# 3. Enrollment Count Per Program
class EnrollmentPerProgramView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Enrollment.objects.values('course__program__name').annotate(total=Count('id'))
        return Response(data)

# 4. Attendance Distribution (Absent/Present)
class AttendanceDistributionView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Attendance.objects.values('status').annotate(count=Count('id'))
        return Response(data)

# 5. Grades Distribution
class GradesDistributionView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Grade.objects.values('grade').annotate(count=Count('id')).order_by('-grade')
        return Response(data)

# 6. Withdrawals per Course
class WithdrawalsPerCourseView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Withdrawal.objects.values('course__name').annotate(total=Count('id')).order_by('-total')
        return Response(data)

# 7. Top Performing Students (GPA)
class TopPerformingStudentsView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Grade.objects.values('student__user__username').annotate(gpa=Avg('grade')).order_by('-gpa')[:10]
        return Response(data)

# 8. Students with Low Attendance
class LowAttendanceStudentsView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = (
            Attendance.objects.filter(status='absent')
            .values('student__user__username')
            .annotate(absences=Count('id'))
            .order_by('-absences')[:10]
        )
        return Response(data)

# 9. Popular Courses (by enrollment)
class PopularCoursesView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Enrollment.objects.values('course__name').annotate(total=Count('id')).order_by('-total')[:10]
        return Response(data)

class FacultyTeachingLoadView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Course.objects.values('faculty__user__username').annotate(total_courses=Count('id')).order_by('-total_courses')
        return Response(data)

class TopStudentsByDepartmentView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request, program_id):
        departments = Department.objects.filter(program__id=program_id)
        data = []

        for department in departments:
            top_students = (
                Grade.objects
                .filter(student__department=department)
                .values('student__user__id', 'student__user__username')
                .annotate(gpa=Avg('grade'))
                .order_by('-gpa')[:3]  # Top 3 students
            )
            data.append({
                'department': department.name,
                'top_students': top_students
            })

    
        return Response(data)
    
class AverageGradesByDepartmentView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
       
        data = Grade.objects.values('student__program__department__name') \
            .annotate(average_grade=Avg('grade')) \
            .order_by('-average_grade')

        response = [
            {
                "department": entry['student__program__department__name'],
                "average_grade": round(entry['average_grade'], 2) if entry['average_grade'] else None
            }
            for entry in data
        ]
        return Response(response)
    
class WithdrawalRateByDepartmentView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [AdminThrottle]


    def get(self, request):
        data = Withdrawal.objects.values('student__program__department__name') \
            .annotate(total_withdrawals=Count('id')) \
            .order_by('-total_withdrawals')

        response = [
            {
                "department": entry['student__program__department__name'],
                "withdrawals": entry['total_withdrawals']
            }
            for entry in data
        ]
        return Response(response)
    

class EnrollmentTrendsByProgramView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [AdminThrottle]


    def get(self, request):
        data = Enrollment.objects.values('program__name', 'academic_year') \
            .annotate(total_enrolled=Count('id')) \
            .order_by('program__name', 'academic_year')

        response = [
            {
                "program": entry['program__name'],
                "academic_year": entry['academic_year'],
                "total_enrolled": entry['total_enrolled']
            }
            for entry in data
        ]
        return Response(response)

class AttendanceSummaryByDepartmentView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [AdminThrottle]


    def get(self, request):
        data = Attendance.objects.values('student__program__department__name') \
            .annotate(avg_attendance=Avg('attendance_percentage')) \
            .order_by('-avg_attendance')

        response = [
            {
                "department": entry['student__program__department__name'],
                "average_attendance": round(entry['avg_attendance'], 2) if entry['avg_attendance'] else None
            }
            for entry in data
        ]
        return Response(response)
    
class TopCoursesByProgramView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request, program_id):
        data = Grade.objects.filter(student__program__id=program_id) \
            .values('course__name') \
            .annotate(avg_grade=Avg('grade')) \
            .order_by('-avg_grade')[:5]  # Top 5 courses

        response = [
            {
                "course": entry['course__name'],
                "average_grade": round(entry['avg_grade'], 2) if entry['avg_grade'] else None
            }
            for entry in data
        ]
        return Response(response)

class LowPerformingStudentsByProgramView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request, program_id):
        data = Grade.objects.filter(student__program__id=program_id) \
            .values('student__id', 'student__user__first_name', 'student__user__last_name') \
            .annotate(avg_grade=Avg('grade')) \
            .filter(avg_grade__lt=50) \
            .order_by('avg_grade')  # Assuming <50 is low performance

        response = [
            {
                "student_id": entry['student__id'],
                "name": f"{entry['student__user__first_name']} {entry['student__user__last_name']}",
                "average_grade": round(entry['avg_grade'], 2)
            }
            for entry in data
        ]
        return Response(response)
    
class StudentsPerProgramView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Student.objects.values('program__name').annotate(total=Count('id')).order_by('-total')
        return Response(data)
class FacultyPerProgramView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Faculty.objects.values('program__name').annotate(total=Count('id')).order_by('-total')
        return Response(data)

class AverageGradesByProgramView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Grade.objects.values('student__program__name') \
            .annotate(average_grade=Avg('grade')) \
            .order_by('-average_grade')

        response = [
            {
                "program": entry['student__program__name'],
                "average_grade": round(entry['average_grade'], 2) if entry['average_grade'] else None
            }
            for entry in data
        ]
        return Response(response)
class WithdrawalRateByProgramView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Withdrawal.objects.values('student__program__name') \
            .annotate(total_withdrawals=Count('id')) \
            .order_by('-total_withdrawals')

        response = [
            {
                "program": entry['student__program__name'],
                "withdrawals": entry['total_withdrawals']
            }
            for entry in data
        ]
        return Response(response)

class AttendanceSummaryByProgramView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request):
        data = Attendance.objects.values('student__program__name') \
            .annotate(avg_attendance=Avg('attendance_percentage')) \
            .order_by('-avg_attendance')

        response = [
            {
                "program": entry['student__program__name'],
                "average_attendance": round(entry['avg_attendance'], 2) if entry['avg_attendance'] else None
            }
            for entry in data
        ]
        return Response(response)
class TopStudentsByProgramView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [AdminThrottle]

    def get(self, request, program_id):
        top_students = (
            Grade.objects
            .filter(student__program__id=program_id)
            .values('student__user__id', 'student__user__first_name', 'student__user__last_name')
            .annotate(gpa=Avg('grade'))
            .order_by('-gpa')[:3]
        )

        response = [
            {
                "student_id": entry['student__user__id'],
                "name": f"{entry['student__user__first_name']} {entry['student__user__last_name']}",
                "gpa": round(entry['gpa'], 2)
            }
            for entry in top_students
        ]
        return Response(response)


