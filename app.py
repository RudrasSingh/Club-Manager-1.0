from flask import *
from pyrebase import *
from time import sleep
from flask import request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random 
#-----------------setting up the app------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.secret_key = 'SECRET_KEY' #generate a secret key and use it here in this virtual env

#------------------------Database setup-----------------------------




#------------------------firebase setting---------------------------



#------------------- Routing ------------------------
@app.route('/')
def landingPage():
    return render_template('index.html')

@app.route('/aboutus')
def aboutusPage():
    return render_template('about.html')

@app.route('/login')
def signupPage():
    return render_template('signup.html')

@app.route('/verification')
def otp_verification():
    return render_template('otp.html')


@app.route('/')
def homepage():
    return redirect('index.html')



#------------------------otp---------------------------
otp_store = {}  

def generate_otp():
    return random.randint(1000, 9999)  

def send_otp_email(receiver_email, otp):
    sender_email = "your_email@gmail.com"  #Clubsync email address to be added 
    password = "your_password"              #password of the email to be added 

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Your OTP"

    body = f"Your OTP is: {otp}"
    message.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

@app.route('/request_otp', methods=['POST'])
def request_otp():
    email_address = request.json.get('email_address')

    otp = generate_otp()
    otp_store[email_address] = otp  # Store OTP in memory

    send_otp_email(email_address, otp)

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
    

