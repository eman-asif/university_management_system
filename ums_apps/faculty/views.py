from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from faculty.models import Faculty
from faculty.serializers import FacultySerializer
from utils import get_user_throttle

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
        return Faculty.objects.all()

    def get_throttles(self):
        return get_user_throttle(self.request.user)
