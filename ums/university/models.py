from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Program(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    faculty = models.ForeignKey('Faculty', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    enrollment_date = models.DateField()

    def __str__(self):
        return self.user.username

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateField(auto_now_add=True)

class Withdrawal(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    reason = models.TextField()
    date = models.DateField(auto_now_add=True)
    
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField()

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])

class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
