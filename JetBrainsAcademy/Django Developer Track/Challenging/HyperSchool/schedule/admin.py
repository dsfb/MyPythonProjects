from django.contrib import admin
from . import models

admin.site.register([models.Course, models.Student, models.Teacher])
