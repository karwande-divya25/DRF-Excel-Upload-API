import openpyxl

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation

from .models import Student


@api_view(['POST'])
def upload_student_excel(request):

    file = request.FILES.get('file')

    if not file:
        return Response(
            {"error": "File is required"},
            status=400
        )

    if not file.name.lower().endswith('.xlsx'):
        return Response(
            {"error": "Only .xlsx files are allowed"},
            status=400
        )

    if file.size == 0:
        return Response(
            {"error": "Uploaded file is empty"},
            status=400
        )

    try:
        workbook = openpyxl.load_workbook(file, data_only=True)
        sheet = workbook.active
    except Exception:
        return Response(
            {"error": "Unable to read Excel file"},
            status=400
        )

    total_rows = 0
    inserted_count = 0
    errors = []

    allowed_courses = [
        "Java",
        "Python",
        "Testing",
        "Data Analytics"
    ]

    excel_emails = set()
    excel_mobiles = set()

    for row_number, row in enumerate(
        sheet.iter_rows(min_row=2, values_only=True),
        start=2
    ):

        if all(value is None for value in row):
            continue

        total_rows += 1

        student_name = str(row[0]).strip() if row[0] is not None else ""
        email = str(row[1]).strip() if row[1] is not None else ""
        mobile = str(row[2]).strip() if row[2] is not None else ""
        course = str(row[3]).strip() if row[3] is not None else ""
        city = str(row[4]).strip() if row[4] is not None else ""
        fees = row[5]

        row_errors = []

        if not student_name:
            row_errors.append("Student name is required")
        elif len(student_name) < 3:
            row_errors.append(
                "Student name must contain at least 3 characters"
            )

        if not email:
            row_errors.append("Email is required")
        else:
            try:
                validate_email(email)
            except ValidationError:
                row_errors.append("Invalid email format")

            if email.lower() in excel_emails:
                row_errors.append(
                    "Email already exists in Excel file"
                )

            if Student.objects.filter(email__iexact=email).exists():
                row_errors.append(
                    "Email already exists in database"
                )

        if not mobile:
            row_errors.append("Mobile number is required")
        elif not mobile.isdigit() or len(mobile) != 10:
            row_errors.append(
                "Mobile number must contain exactly 10 digits"
            )

        if mobile in excel_mobiles:
            row_errors.append(
                "Mobile number already exists in Excel file"
            )

        if Student.objects.filter(mobile=mobile).exists():
            row_errors.append(
                "Mobile number already exists in database"
            )

        if course not in allowed_courses:
            row_errors.append(
                "Invalid course. Allowed: Java, Python, Testing, Data Analytics"
            )

        if not city:
            row_errors.append("City is required")

        try:
            fee_value = Decimal(str(fees))

            if fee_value <= 0:
                row_errors.append("Fees must be greater than 0")

        except (InvalidOperation, ValueError, TypeError):
            row_errors.append("Fees must be numeric")

        if row_errors:

            error_data = {
                "row": row_number,
                "errors": row_errors
            }

            if email:
                error_data["email"] = email

            if mobile:
                error_data["mobile"] = mobile

            errors.append(error_data)

            continue

        Student.objects.create(
            student_name=student_name,
            email=email,
            mobile=mobile,
            course=course,
            city=city,
            fees=fee_value
        )

        inserted_count += 1

        excel_emails.add(email.lower())
        excel_mobiles.add(mobile)
        
    if total_rows == 0:
     return Response(
    {"error": "Excel file is empty"},
     status=400
        )
        

    return Response({
        "message": "Excel processing completed",
        "total_rows": total_rows,
        "inserted_count": inserted_count,
        "failed_count": len(errors),
        "errors": errors
    })