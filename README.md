DDSS (Dynamic Delivery Scheduling System)

Project Overview

DDSS is an AI-enabled monitoring and visualization platform developed to track supplier deliveries, monitor production schedules, identify delivery risks, and provide real-time dashboards for manufacturing operations.

The application consists of multiple Streamlit dashboards:

- Main Dashboard
- Supplier Portal Screen
- TV Monitoring Screen
- Risk Analysis Module
- Delivery Accuracy Module
- DS Time Monitoring Module

---

Technology Stack

Frontend

- Streamlit

Backend

- Python

Database

- Microsoft SQL Server
- SQLAlchemy
- PyODBC

Data Processing

- Pandas
- NumPy

---

Project Structure

DDSS/

├── app.py

├── pages/

│ ├── portal_screen.py

│ ├── tv_screen.py

│ └── other modules

├── services/

│ ├── supplier_accuracy.py

│ ├── supplier_ds_time.py

│ ├── supplier_risk.py

│ └── other services

├── database/

│ └── load_to_sql.py

├── data/

│ └── input excel files

├── .env

├── requirements.txt

└── README.md

---

Prerequisites

Install:

- Python 3.10+
- Microsoft SQL Server
- SQL Server Management Studio (SSMS)
- ODBC Driver 17 for SQL Server

---

Installation

Clone repository:

git clone <repository-url>

cd DDSS

Install dependencies:

pip install -r requirements.txt

---

Environment Configuration

Create a ".env" file in project root:

DB_SERVER=YOUR_SERVER_NAME

DB_NAME=DDSS

DB_USER=YOUR_USERNAME

DB_PASSWORD=YOUR_PASSWORD

INPUT_FOLDER=data

OUTPUT_FOLDER=output

Do not store passwords or database credentials directly in source code.

---

Database Setup

Create SQL Server database:

CREATE DATABASE DDSS;

Update environment variables with correct SQL Server details.

Load source Excel data into SQL Server using:

python database/load_to_sql.py

---

Running the Application

Start Streamlit application:

streamlit run app.py

Application will be available at:

http://localhost:8501

---

Available Screens

Main Dashboard

Provides overall delivery monitoring and supplier analytics.

Supplier Portal Screen

Displays supplier-specific information and operational metrics.

TV Screen

Displays lot-wise delivery status and production monitoring information.

---

Input Data

Source files are placed inside:

data/

Supported formats:

- Excel (.xlsx)
- Excel (.xls)

---

Output

The system generates:

- Supplier delivery performance metrics
- Risk analysis reports
- Delivery schedule monitoring dashboards
- Lot status visualization

---

Security Notes

- Store credentials only in ".env"
- Never commit ".env" files to GitHub
- Repository must remain private
- Sensitive data must be excluded through ".gitignore"

---

Author

Sasank Kari

DDSS Project