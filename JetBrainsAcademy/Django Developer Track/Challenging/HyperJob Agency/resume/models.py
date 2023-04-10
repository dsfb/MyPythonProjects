from django.conf import settings
from django.db import models


class Resume(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)

    class Meta:
        db_table = 'resume_resume'