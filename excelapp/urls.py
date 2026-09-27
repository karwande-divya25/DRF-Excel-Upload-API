from django.urls import path
from .views import upload_student_excel


urlpatterns = [
    path('students/upload-excel', upload_student_excel),
]