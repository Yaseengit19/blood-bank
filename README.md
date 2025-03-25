Blood Bank
A Django-based Blood Bank management system that allows users to donate and request blood donations. This application aims to simplify the management of blood donation records and streamline the process of helping those in need of blood.

Prerequisites
Python 3.7.6 (provided with the folder)

pip (Python package installer)

Steps to Run the Program
Follow these steps to get the project running on your local machine:

1. Clone the repository:
First, clone the project repository to your local machine.

>>bash
git clone https://github.com/yourusername/blood-bank.git
cd blood-bank
2. Set up a virtual environment (if needed):
If you need to set up a virtual environment, you can create and activate one. Make sure you're using Python version 3.7.6 (provided with the folder). Here’s how to do it:

For Windows:

>>bash
python3.7 -m venv venv
.\venv\Scripts\activate
For macOS/Linux:

>>bash
python3.7 -m venv venv
source venv/bin/activate
Once the virtual environment is activated, your terminal prompt should show the environment name (e.g., (venv)).

3. Install the required dependencies:
Install the necessary Python packages listed in requirements.txt:

>>bash
pip install -r requirements.txt

4. Apply migrations:
Before running the server, you'll need to apply the database migrations:

>>bash
python manage.py makemigrations
python manage.py migrate

This will set up the database tables based on your models.

5. Run the development server:
Once everything is set up, you can run the Django development server:

>>bash
python manage.py runserver
The server should start running locally, and you can access the application at:

http://127.0.0.1:8000/

Admin Panel :
If you want to access the Django admin panel, you’ll need to create a superuser (admin account) to log in:

>>bash

python manage.py createsuperuser

User Features:
>>Donors: Users can register as blood donors and specify the blood group they are willing to donate,request blood, recieve donation-request from patients of the same blood group ,schedule donations on registered hospitals.

>>Patient: Users can submit a request for blood , view availability og the blood group in blood bank , view matching blood donors and also send requests for donation.

>>Hospital: Users can submit bulk and emergency requests to blood bank(Admin) , approve scheduled donation-request from donors.

>>Functionality: View all donors based on blood type and location .

Admin Features:
Manage Donors: Admin can add, update, or delete donor records.

Manage Patients(Requester): Admin can manage blood requests from users.

Manage Hospitals :Admin can manage requests from hospitals.

Development
To contribute to the development of this project, follow these steps:

Fork the repository and clone it to your local machine.

Create a new branch for your feature or fix.

Install the required dependencies by running pip install -r requirements.txt.

Make your changes and test locally.

Commit your changes with a clear and concise message.

Push your changes to your fork and open a pull request to the main repository.

Notes:
Make sure you have Python 3.7.6 installed before proceeding with the steps above. This is critical to ensure compatibility with your environment and dependencies.

The project’s requirements.txt file should include all the necessary Python packages for Django and any other dependencies.

You may want to add more sections for additional features or deployment steps, depending on the project's specifics (e.g., deploying to Heroku or AWS).
