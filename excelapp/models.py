from django.db import models

# Create your models here.
from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    salary = models.IntegerField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class Student(models.Model):
    student_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    course = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name