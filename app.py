from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import csv
import requests
import os
from dotenv import load_dotenv
import mariadb
import urllib.parse

load_dotenv()
app = Flask(__name__)

if os.getenv('JAWSDB_MARIA_URL'):
    # Heroku environment
    url = os.getenv('jawsDB_MARIA_URL')
    parsed_url = urllib.parse.urlparse(url)
    app.config['MYSQL_HOST'] = parsed_url.hostname
    app.config['MYSQL_USER'] = parsed_url.username
    app.config['MYSQL_PASSWORD'] = parsed_url.password
    app.config['MYSQL_DB'] = parsed_url.path[1:]  # Remove leading slash from the path
else:
    # Connect to MySQL database server - Required
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'default_user')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'default_password')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'usersDB')
    app.config['MYSQL_PORT'] = 3306


mysql = MySQL(app)

# External API URL
api_url = "https://tech-interview-api-ultramed.vercel.app/users"


def fetch_users(api_url):
    """
    Get data from external API.
    :param: The API url to fetch data from
    :return: A list of dictionaries
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad status codes
        api_data = response.json()
        # print(api_data)
        return api_data
    except requests.RequestException as e:
        print(f"Error fetching users: {e}")
        return []


def get_api_data_keys(data):
    """
    Extract keys from the first entry of API data (in this case no nesting keys).
    :param data: List of dictionaries from API response
    :return: List of keys found in API
    """
    if isinstance(data, list) and data:
        # print(list(data[0].keys()))
        return list(data[0].keys())
    return []


def write_to_csv(file_name="user_list.csv"):
    """
    Write API data to a CSV file. The data in the CSV file is used to create the database in MySQL.
    The table in the MySQL database was created within MySQL using import from CSV file.
    :param: file_name: CSV file name to save API data. Default to user_list
    """
    try:
        # Get API data
        data = fetch_users(api_url)
        # print(data)
        if not data:
            return "No data available to write to CSV."

        # Get the field names (headers) made up from API keys
        field_names = get_api_data_keys(data)
        # print(field_names)

        # Write to the CSV file
        with open(file_name, "w", newline="") as file:
            spreadsheet = csv.DictWriter(file, fieldnames=field_names)
            spreadsheet.writeheader()
            spreadsheet.writerows(data)
        return "Data successfully written to user_list.csv."

    except requests.RequestException as e:
        return f"Error fetching API data: {e}"
    except IOError as e:
        return f"Error writing to CSV: {e}"


# Call function to write to CSV file
write_to_csv()


# Route to render login page
@app.route("/")
def login():
    return render_template("login.html")


# Route to render main page containing users list
@app.route('/main')
def main():
    try:
        # Query the database to get all users
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user_list")
        user_list = cur.fetchall()
        cur.close()
        if not user_list:
            print("No users found in the database.")

        return render_template('main.html', user_list=user_list)
    except Exception as e:
        return f"Error: {str(e)}"


# Route to render edit page
@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    try:
        cur = mysql.connection.cursor()

        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            status = request.form['status']

            # Update the user details in the database
            cur.execute("""
                UPDATE user_list
                SET name = %s, email = %s, status = %s
                WHERE id = %s
            """, (name, email, status, id))

            mysql.connection.commit()

            # Redirect back to main page after updating user
            return redirect(url_for('main'))

        # Get the user data from database to pre-fill the form using GET request
        cur.execute("SELECT * FROM user_list WHERE id = %s", (id,))
        user = cur.fetchone()  # Fetch the user data based on ID

        if user is None:
            # Handles the case where user is not found for the given ID
            return "User not found", 404

        return render_template('edit_user.html', user=user)
    except Exception as e:
        return f"Error: {str(e)}", 500  # server error
    finally:
        cur.close()


# Route to render page to add users
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            status = request.form['status']

            # Add a user to the user_list table in the database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user_list (name, email, status) VALUES (%s, %s, %s)", (name, email, status))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('main'))

        return render_template('add_user.html')
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    # Delete the user with the given ID from user_list table in database
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM user_list WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True)