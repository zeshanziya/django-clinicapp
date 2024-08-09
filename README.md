# Clinic Booking System

This is a Django-based web application for managing clinic appointments. It allows patients to book, view, and cancel appointments, and staff to manage bookings.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Virtualenv (optional, but recommended)

### Getting Started

1. **Clone the repository:**
    ```sh
    git clone https://github.com/zeshanziya/django-clinicapp/
    cd clinic-booking-system
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run migrations to set up the database:**
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser to access the admin panel:**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

7. **Access the application:**
    - Open your web browser and go to `http://127.0.0.1:8000/` to view the home page.
    - Go to `http://127.0.0.1:8000/admin/` to access the admin panel (login with the superuser credentials).

8. **Setup Email**

    1. Go to myaccount.google.com
    2. Ensure that 2FA is enabled.
    3. In the search bar, search for App Passwords or search for App Passwords under Security.
    4. Create a new App Password by giving the app and then hit create.
    5. You will be able to see a password. Copy it and use it in `.env`

9. Setup env file.

    - Copy `.env-sample` to `.env`.
    - Update values as below.
        - `EMAIL_HOST_USER` as your email.
        - `EMAIL_HOST_PASSWORD` as password created in previous step.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
