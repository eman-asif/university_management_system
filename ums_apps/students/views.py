from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from students.models import Student, Enrollment, Withdrawal, Grade, Attendance
from students.serializers import StudentSerializer, EnrollmentSerializer, WithdrawalSerializer, GradeSerializer, AttendanceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Count
from utils import get_user_throttle

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
        return Student.objects.all()

    def get_throttles(self):
        return get_user_throttle(self.request.user)

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
        return Enrollment.objects.all()

    def get_throttles(self):
        return get_user_throttle(self.request.user)

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
        return Withdrawal.objects.all()

    def get_throttles(self):
        return get_user_throttle(self.request.user)

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
        return Grade.objects.all()

    def get_throttles(self):
        return get_user_throttle(self.request.user)

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
        return Attendance.objects.all()

    def get_throttles(self):
        return get_user_throttle(self.request.user)