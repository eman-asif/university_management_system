from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Avg, Count
from .models import Department, Program, Course, Student, Faculty, Enrollment, Withdrawal, Grade, Attendance, Timetable
from .serializers import DepartmentSerializer, ProgramSerializer, CourseSerializer, StudentSerializer, FacultySerializer, EnrollmentSerializer, WithdrawalSerializer, GradeSerializer, AttendanceSerializer, TimetableSerializer
from rest_framework.permissions import DjangoModelPermissions


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'faculty':
            return Course.objects.filter(faculty__user=user)
        elif user.user_type == 'student':
            return Course.objects.filter(enrollment__student__user=user).distinct()
        # elif user.is_superuser:
        #     return Course.objects.all()
        return Course.objects.all()

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'student':
            return Student.objects.filter(user=user)
        elif user.user_type == 'faculty':
            return Student.objects.filter(enrollment__course__faculty__user=user).distinct()
        # elif user.is_superuser:
        #     return Student.objects.all()
        return Student.objects.all()

class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'faculty':
            return Faculty.objects.filter(department=user.faculty.department)
        elif user.user_type == 'student':
            return Faculty.objects.filter(department=user.student.department)
        # elif user.is_superuser:
        #     return Faculty.objects.all()
        return Faculty.objects.all()

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'faculty':
            return Enrollment.objects.filter(course__faculty__user=user)
        elif user.user_type == 'student':
            return Enrollment.objects.filter(student__user=user)
        # elif user.is_superuser:
        #     return Enrollment.objects.all()
        return Enrollment.objects.all()

class WithdrawalViewSet(viewsets.ModelViewSet):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'faculty':
            return Withdrawal.objects.filter(course__faculty__user=user)
        elif user.user_type == 'student':
            return Withdrawal.objects.filter(student__user=user)
        # elif user.is_superuser:
        #     return Withdrawal.objects.all()
        return Withdrawal.objects.all()

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'faculty':
            return Grade.objects.filter(course__faculty__user=user)
        elif user.user_type == 'student':
            return Grade.objects.filter(student__user=user)
        # elif user.is_superuser:
        #     return Grade.objects.all()
        return Grade.objects.all()

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'faculty':
            return Attendance.objects.filter(course__faculty__user=user)
        elif user.user_type == 'student':
            return Attendance.objects.filter(student__user=user)
        # elif user.is_superuser:
        #     return Attendance.objects.all()
        return Attendance.objects.all()

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'faculty':
            return Timetable.objects.filter(course__faculty__user=user)
        elif user.user_type == 'student':
            return Timetable.objects.filter(course__enrollment__student__user=user).distinct()
        # elif user.is_superuser:
        #     return Timetable.objects.all()
        return Timetable.objects.all()

class StudentGPAView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        gpa_data = (
            Grade.objects.values('student__user__username')
            .annotate(gpa=Avg('grade'))
            .order_by('-gpa')
        )
        return Response(gpa_data)

class CourseWithdrawalsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = (
            Withdrawal.objects.values('course__code', 'course__name')
            .annotate(total_withdrawals=Count('id'))
            .order_by('-total_withdrawals')
        )
        return Response(data)

class AttendanceSummaryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = (
            Attendance.objects.filter(status='absent')
            .values('student__user__username', 'course__code', 'course__name')
            .annotate(absences=Count('id'))
            .order_by('-absences')
        )
        return Response(data)