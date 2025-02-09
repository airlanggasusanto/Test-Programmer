# Test Programmer
A simple Django-based web application for the FastPrint programmer test. The application manages product data through API integration, stores it in PostgreSQL, and provides basic CRUD operations.

## Dependecy
- Django Framework 5.1.6
- Python 3.12.2
- PostgreSQL 17.2.3
- HTML, CSS, JavaScript
- Tailwind

## Installation and Configuration
Follow these steps to install and configure the Django-based application.

```sh
# Clone the repository
git clone https://github.com/airlanggasusanto/Test-Programmer.git
cd Test-Programmer

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your .env file (create it manually and configure environment variables)

# Create the static directory
mkdir static  # On Windows use: md static

# Apply database migrations
python manage.py migrate

# Fetch products via API (run only once)
python manage.py fetch_data

# Run the development server
python manage.py runserver