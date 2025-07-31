from django.db import models

class Faculty(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE)
    department = models.ForeignKey('academics.Department', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
