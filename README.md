# Computer Lab Borrower System

## Project Overview

This project is designed to streamline the borrowing process in our computer lab. It allows users to borrow computers, monitors, and other equipment efficiently. The system tracks borrowers and the items they check out, reducing the need for manual logging.

## Features

- User-friendly interface for tracking equipment and borrowers.
- Real-time borrowing logs.

## Requirements

- Python 3.x
- Django
- SQLite (for database)
- pillow & opencv (for image processing)
- Tesseract

## Installation

- Clone this repository:
  ```bash
    git clone https://github.com/CSSO-Linux-User-Group-ESSU/Computer-lab-borrower-system.git
  ```
- Navigate to the project directory:
  ```bash
    cd Computer-lab-borrower-system
  ```
- Install dependencies:
  ```bash
    pip install -r requirements.txt
  ```
- Run the server:
  ```bash
    python manage.py runserver
  ```

## Usage

- Access the system by navigating to http://127.0.0.1:8000/.
- Log in with your credentials or sign up as a new user.
- Admins can manage devices and users from the admin panel.
