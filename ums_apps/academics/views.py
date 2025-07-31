from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from academics.models import Department, Program, Course, Timetable
from academics.serializers import DepartmentSerializer, ProgramSerializer, CourseSerializer, TimetableSerializer
from utils import get_user_throttle
import pdb

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_throttles(self):
        return get_user_throttle(self.request.user)

class ProgramViewSet(viewsets.ModelViewSet):

    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticated]

    def get_throttles(self):
        return get_user_throttle(self.request.user)

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
        return Course.objects.all()

    def get_throttles(self):
        return get_user_throttle(self.request.user)

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
        return Timetable.objects.all()

    def get_throttles(self):
        return get_user_throttle(self.request.user)
