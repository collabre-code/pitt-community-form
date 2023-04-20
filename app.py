#from asyncio import Runner
from flask import Flask, render_template, request
import pyodbc
import os

# create an instance of the Flask class
app = Flask(__name__)

# configure the SQL database connection

print('Connecting to Azure SQL DataBase.........')
print(pyodbc.drivers())
#connect to azure database
os.environ["ODBCSYSINI"] = "/home/collabre85"

server = 'collabserver.database.windows.net'
database = 'collabDataBase'
username = 'collabuser'
password = 'YTc@3364'
#driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)



# define the route for the form page
@app.route('/')
def form():
    return render_template('form.html')

# define the route for processing form submission
@app.route('/submit', methods=['POST'])
def submit():

    

    # get the user input from the form
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    phone = request.form['phone']
    user_type = request.form['type_dropdown']
    location = request.form['location_dropdown']
    expertise = request.form['areaofknowledge']
    institute_assoc = request.form['institutes']
    personal_assoc = request.form['personals']
    past_interactions = request.form['interactions']

    #get submarkets from form
    markets = request.form.getlist('markets[]')
    markets_str = ','.join(markets)

    #get stages of involvement from form
    stages = request.form.getlist('stages[]')
    stages_str = ','.join(stages)

    #get needs from form
    needs = request.form.getlist('needs_dropdown[]')
    needs_str = ','.join(needs)


    # insert the user input into the database
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO COMMUNITYDATABASE (firstname, lastname, email, phone, user_type, industry_submarket, stages_of_involvement, pittsburg_location, areas_of_expertise, needs, institutional_assoc, personal_assoc, past_interactions) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", firstname, lastname, email, phone, user_type, markets_str, stages_str, location, expertise, needs_str, institute_assoc, personal_assoc, past_interactions)
    cnxn.commit()

    # return a response to the user
    return 'Data Submitted Successfully!'

if __name__ == '__main__':
    app.run()
