from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    csv_file = models.FileField(upload_to='project_files')

    def __str__(self):
        return self.name