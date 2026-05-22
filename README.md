# FIPE Vehicle Price Search API

A web application built with Flask and Pandas to process Excel spreadsheets and retrieve vehicle price data from the FIPE API.

The application allows users to upload an Excel file containing vehicle information and automatically generates another spreadsheet with:

- Current FIPE price
- Vehicle details
- Fuel type
- FIPE code
- Historical FIPE prices
- Historical reference months

The project uses the FIPE API v2 maintained by Deivid Fortuna.

---

# Features

- Upload Excel spreadsheets
- Search multiple vehicles automatically
- Retrieve FIPE data by:
  - Brand
  - Model
  - Year
- Retrieve historical FIPE prices
- Export processed results to Excel
- Error handling for invalid vehicles
- Clean and organized spreadsheet output

---

# Technologies

- Python 3
- Flask
- Pandas
- Requests
- OpenPyXL

---

# FIPE API Documentation

Official API documentation:

https://deividfortuna.github.io/fipe/v2/#tag/Fipe/operation/GetReferences

GitHub repository:

https://github.com/deividfortuna/fipe

---

# Project Structure

```bash
fipe_project/
│
├── app.py
├── requirements.txt
│
├── services/
│   └── fipe_service.py
│
├── templates/
│   └── index.html
│
├── uploads/
│
├── outputs/
│
└── static/
    └── style.css
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/your-username/fipe_project.git
```

---

## Create virtual environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

Create a `requirements.txt` file:

```txt
flask
pandas
requests
openpyxl
```

---

# Running the Application

```bash
python app.py
```

The application will run at:

```txt
http://127.0.0.1:5000
```

---

# Input Spreadsheet Format

The uploaded Excel file must contain the following columns:

| Brand | Model | Year |
|---|---|---|
| Toyota | Corolla | 2020 |
| Renault | Boreal Evolution 1.3 Turbo 16V 5p Aut. | 2026 |

Column names are case-insensitive.

---

# Output Spreadsheet Example

| Brand | Model | Year | Current FIPE Price | History Month | History Price |
|---|---|---|---|---|---|
| Renault | Boreal Evolution | 2026 | R$ 158.983,00 | maio de 2026 | R$ 158.983,00 |
| Renault | Boreal Evolution | 2026 | R$ 158.983,00 | abril de 2026 | R$ 156.511,00 |

---

# Supported Data

The application retrieves:

- Brand
- Model
- Year
- Fuel
- FIPE code
- Current FIPE price
- Reference month
- Historical FIPE prices

---

# Error Handling

The system handles:

- Brand not found
- Model not found
- Year not found
- API request failures
- Invalid spreadsheet columns

---

# API Endpoints Used

## Get Brands

```http
GET /cars/brands
```

---

## Get Models

```http
GET /cars/brands/{brand_id}/models
```

---

## Get Years

```http
GET /cars/brands/{brand_id}/models/{model_id}/years
```

---

## Get Vehicle Price

```http
GET /cars/brands/{brand_id}/models/{model_id}/years/{year_id}
```

---

## Get Vehicle Price History

```http
GET /cars/{fipe_code}/years/{year_id}/history
```

---

# Credits

FIPE API maintained by Deivid Fortuna.

Documentation:

https://deividfortuna.github.io/fipe/v2/#tag/Fipe/operation/GetReferences
