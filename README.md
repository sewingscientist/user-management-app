## User Management Web App

This Flask-based application provides a user management system with functionalities to view, add, edit, and delete users. 
Data is fetched from an external API and stored in a MySQL database. The app includes a dynamic frontend with sorting and 
filtering using DataTables and ensures secure database operations. Ideal for managing user data in a simple and efficient way.

You may set up your own database within MySQl if needed. Instructions to do this can be found in the __database__ folder as
*userDB.sql*

####  1. Create project environment
- Create project folder within your IDE/local system
- Create a virtual environment:

*python -m venv venv*

- Activate the virtual environment (dependent on operating system):

`venv/Scripts/activate` (Windows)

`source venv/Scripts/activate` (Linux, macOS)

- Install dependencies:

*pip install -r requirements.txt*

#### 2. In order not to share your MySQL database credentials, create a .env file as follows:

- In your app.py file:

`import os`

`from flask import Flask`

`from flask_mysqldb import MySQL`

`app = Flask(__name__)`

- Configure MySQL using environment variables:

`app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')`

`app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')`

`app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'default_password')`

`app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'default_db')`

`mysql = MySQL(app)`

- Within the main project root directory, create a .env file (no extension) to store environment variables locally 
__(do not share this file).__ Add .env to your .gitignore. Replace values below in your .env with your mySQL credentials:

MYSQL_HOST = *'localhost'*

MYSQL_USER = *'yourMySQLUser'*

MYSQL_PASSWORD = *'yourPassword'*

MYSQL_DB = *'yourDatabaseName'*

- Use a library like *python-dotenv* to load the .env file in development, run:

*pip install python-dotenv*

- Add this at the start of your app.py file:

`from dotenv import load_dotenv`

`load_dotenv()`
