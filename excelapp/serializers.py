from rest_framework import serializers
from .models import Employee

from .models import Employee, Student
class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'salary', 'department']
        
        
        
        
        

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = [
            'id',
            'student_name',
            'email',
            'mobile',
            'course',
            'city',
            'fees',
            'created_at'
        ]