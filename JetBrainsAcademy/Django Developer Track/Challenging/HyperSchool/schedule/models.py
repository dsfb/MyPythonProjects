from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=100)
    age = models.IntegerField()
    about = models.TextField()

    def __str__(self):
        return f"Teacher({self.name}, {self.surname}, {self.age}, {self.about})"


class Course(models.Model):
    title = models.CharField(max_length=255)
    info = models.CharField(max_length=1000)
    duration_months = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    teacher = models.ManyToManyField(Teacher)

    def __str__(self):
        teachers = self.teacher.all()
        teachers_names = ", ".join([teacher.name for teacher in teachers])

        return f"Course(" \
               f"{self.title}, {self.info}, {self.duration_months}, {self.price}, Teachers({teachers_names}))"


class Student(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=100)
    age = models.IntegerField()
    course = models.ManyToManyField(Course)
