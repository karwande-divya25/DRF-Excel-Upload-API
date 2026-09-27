

# DRF Excel Upload API

A Django REST Framework API for uploading student data from an Excel file and validating records row by row.

## Technologies Used

- Python
- Django
- Django REST Framework
- OpenPyXL
- SQLite
- Postman

## Features

- Upload `.xlsx` Excel files through API
- Read Excel data using OpenPyXL
- Validate student records row by row
- Save valid records into the database
- Return validation errors for invalid rows
- API testing using Postman

## API Endpoint

### Upload Student Excel File

**POST**

```text
/api/students/upload-excel
```

### Request

Use `multipart/form-data`.

Key:

```text
file
```

Value:

Excel `.xlsx` file

## Project Structure

```text
DRF_Excel_Project/
│
├── excelapp/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── excelproject/
│   ├── settings.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
└── .gitignore
```

## How to Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API will run locally at:

```text
http://127.0.0.1:8000/
```

## Testing

The API can be tested using Postman by sending a `POST` request with an Excel `.xlsx` file using `multipart/form-data`.

## Author

Divya Karwande
