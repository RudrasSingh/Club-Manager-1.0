from flask import *
from pyrebase import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random 
import database
from dotenv import load_dotenv
import os
#-----------------setting up the app------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.secret_key = 'SECRET_KEY' #generate a secret key and use it here in this virtual env
app.config['EMAIL_USERNAME'] = os.getenv('EMAIL_USERNAME')
app.config['EMAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
load_dotenv()

#------------------------Database setup-----------------------------
@app.before_request
def before_request():
    # Open database connection before each request
    database.connect_to_database()

@app.after_request
def after_request(response):
    # Close database connection after each request
    database.close_connection()
    return response



#------------------------firebase setting---------------------------



#------------------- Routing ------------------------

@app.route('/')
def homepage():
    tag = True #Make this tag True if you want to interact with the after login page for Development purpose
    try:
        if tag is True:
            projects = [
                {
                    'name': 'Envisage',
                    'description': 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Veniam deleniti eaque est error nam. Numquam magni voluptate laborum totam reprehenderit.',
                    'image_url': '/src/jpg/Event posters (1).png',
                    'link': '/static/envi_logo.png'  # Assuming this link is dynamic
                },
                {
                    'name': 'Geekonix',
                    'description': 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Veniam deleniti eaque est error nam. Numquam magni voluptate laborum totam reprehenderit.',
                    'image_url': '/src/jpg/Event posters (1).png',
                    'link': '/static/envi_logo.png'  # Assuming this link is dynamic
                }]
            return render_template('home.html',projects = projects)
        else:
            return render_template('index.html')
    

    except KeyError as e:
        flash(e,"Something went wrong!")

@app.route('/aboutus')
def aboutusPage():
    return render_template('about.html')

@app.route('/login')
def signupPage():
    return render_template('signup.html')

@app.route('/verification')
def otp_verification():
    return render_template('otp.html')

@app.route('/venueBooking')
def venueBook():
    # Pass the list of clubs to the template
    clubs = ["Club A", "Club B", "Club C"]
    colleges = ["Club A", "Club B", "Club C"]
    venues = ["Club A", "Club B", "Club C"]

    return render_template('venuebook.html', clubs = clubs,colleges = colleges,venues = venues)






#------------------------otp verification---------------------------
otp_store = {}  

def generate_otp():
    return random.randint(1000, 9999)  

def send_email(receiver,otp):
    try:
        msg = MIMEText(body)
        msg['Subject'] = "Email verification for Your ClubSync Account"
        msg['From'] = os.getenv("EMAIL_USERNAME")
        msg['To'] = receiver
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD"))
            smtp_server.sendmail(os.getenv("EMAIL_USERNAME"),receiver, msg.as_string())
            print("Message sent!")
    except KeyError as e:
        print(e)


@app.route('/request_otp', methods=['POST'])
def request_otp():
    email_address = request.json.get('email_address')

    otp = generate_otp()
    otp_store[email_address] = otp  # Store OTP in memory

    send_email(email_address, otp)

    return jsonify({'message': 'OTP has been sent to {}'.format(email_address)})


@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    email_address = request.json.get('email_address')
    user_otp = request.json.get('otp')

    if email_address in otp_store and otp_store[email_address] == user_otp:
        del otp_store[email_address]  # Remove OTP from memory after successful verification
        return jsonify({'message': 'OTP verification successful'})
    else:
        return jsonify({'error': 'Invalid OTP'})
    

if __name__ == "__main__":
    app.run(debug=True)
    

