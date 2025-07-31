from django.db import models

class Student(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE)
    department = models.ForeignKey('academics.Department', on_delete=models.SET_NULL, null=True)
    program = models.ForeignKey('academics.Program', on_delete=models.SET_NULL, null=True)
    enrollment_date = models.DateField()

    def __str__(self):
        return self.user.username

class Enrollment(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE)
    enrolled_on = models.DateField(auto_now_add=True)

class Withdrawal(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE)
    reason = models.TextField()
    date = models.DateField(auto_now_add=True)

class Grade(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE)
    grade = models.FloatField()

    def __str__(self):
        return f"{self.student} - {self.course} - {self.grade}"

class Attendance(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])
