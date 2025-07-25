from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Avg, Count
from .models import Department, Program, Course, Student, Faculty, Enrollment, Withdrawal, Grade, Attendance, Timetable
from .serializers import DepartmentSerializer, ProgramSerializer, CourseSerializer, StudentSerializer, FacultySerializer, EnrollmentSerializer, WithdrawalSerializer, GradeSerializer, AttendanceSerializer, TimetableSerializer
from rest_framework.permissions import DjangoModelPermissions

# ModelViewSets
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

        # Admin or superuser sees all
        
        # Faculty: user.id in 42-55
        if user.groups.filter(name='faculty').exists():
            return Course.objects.filter(faculty__user=user)

        # Student: user.id in 2-41
        if user.groups.filter(name='students').exists():
            try:
                student = Student.objects.get(user=user)
                return Course.objects.filter(enrollment__student=student).distinct()
            except Student.DoesNotExist:
                return Course.objects.none()

        # All others see nothing
        return Course.objects.all()
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]
    def get_queryset(self):
        user = self.request.user


        # Faculty: see students enrolled in their courses
        if user.groups.filter(name='faculty').exists():
            return Student.objects.filter(
                enrollment__course__faculty__user=user
            ).distinct()

        # Student: see only their own record
        if user.groups.filter(name='students').exists():
            return Student.objects.filter(user=user)

        # All others see nothing
        return Student.objects.all()
class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]
    def get_queryset(self):
        user = self.request.user

        # Admin: see all faculty
        # Faculty: see faculty in same department
        if user.groups.filter(name='faculty').exists() and hasattr(user, 'faculty'):
            return Faculty.objects.filter(department=user.faculty.department)

        # Student: see faculty in same department
        if user.groups.filter(name='students').exists() and hasattr(user, 'student'):
            return Faculty.objects.filter(department=user.student.department)

        # Others: no access
        return Faculty.objects.all()
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Faculty: enrollments for courses they teach
        if user.groups.filter(name='faculty').exists() and hasattr(user, 'faculty'):
            return Enrollment.objects.filter(course__faculty=user.faculty)

        # Student: their own enrollments
        if user.groups.filter(name='students').exists() and hasattr(user, 'student'):
            return Enrollment.objects.filter(student=user.student)

        # Others: nothing
        return Enrollment.objects.all()

class WithdrawalViewSet(viewsets.ModelViewSet):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        # Faculty sees withdrawals for their taught courses
        if user.groups.filter(name='faculty').exists() and hasattr(user, 'faculty'):
            return Withdrawal.objects.filter(course__faculty=user.faculty)

        # Students see only their own withdrawals
        if user.groups.filter(name='students').exists() and hasattr(user, 'student'):
            return Withdrawal.objects.filter(student=user.student)

        # Default: no access
        return Withdrawal.objects.all()
    
class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        # Faculty can see grades for courses they teach
        if user.groups.filter(name='faculty').exists() and hasattr(user, 'faculty'):
            return Grade.objects.filter(course__faculty=user.faculty)

        # Student can see only their own grades
        if user.groups.filter(name='students').exists() and hasattr(user, 'student'):
            return Grade.objects.filter(student=user.student)

        # Default: no access
        return Grade.objects.all()  
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        
        if user.groups.filter(name='faculty').exists() and hasattr(user, 'faculty'):
            return Attendance.objects.filter(course__faculty=user.faculty)

        if user.groups.filter(name='students').exists() and hasattr(user, 'student'):
            return Attendance.objects.filter(student=user.student)

        return Attendance.objects.all()

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Faculty: view timetables of courses they teach
        if user.groups.filter(name='faculty').exists() and hasattr(user, 'faculty'):
            return Timetable.objects.filter(course__faculty=user.faculty)

        # Student: view timetables of courses they are enrolled in
        if user.groups.filter(name='students').exists() and hasattr(user, 'student'):
            return Timetable.objects.filter(course__enrollment__student=user.student).distinct()

        # Default: no access
        return Timetable.objects.all()
class StudentGPAView(APIView):
    permission_classes = [ IsAdminUser]

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
    permission_classes = [ IsAdminUser]

    def get(self, request):
        data = (
            Attendance.objects.filter(status='absent')
            .values('student__user__username', 'course__code', 'course__name')
            .annotate(absences=Count('id'))
            .order_by('-absences')
        )
        return Response(data)
