from flask import *
from pyrebase import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random 
import database
from dotenv import load_dotenv
import os
from datetime import timedelta
#-----------------setting up the app------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.secret_key = 'SECRET_KEY' #generate a secret key and use it here in this virtual env
app.config['EMAIL_USERNAME'] = os.getenv('EMAIL_USERNAME')
app.config['EMAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
#iguess
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

#--------------session Handling---------------

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.permanent_session_lifetime = timedelta(days=31)



#------------------------firebase setting---------------------------
# firebase_config = {'apiKey': os.getenv('apikey'),
#   'authDomain': os.getenv('authDomain'),
#   'projectId': os.getenv('projectId'),
#   'storageBucket': os.getenv('storageBucket'),
#   'messagingSenderId': os.getenv('messagingSenderId'),
#   'appId': os.getenv('appId'),
#   'measurementId': os.getenv('measurementId'),
#   'databaseURL': ""}
firebase_config = {
  'apiKey': "AIzaSyAJA-UV_R0OHj06NK9LZa90pqTrNelopPc",
  'authDomain': "gyaan-connect-b7b08.firebaseapp.com",
  'projectId': "gyaan-connect-b7b08",
  'storageBucket': "gyaan-connect-b7b08.appspot.com",
  'messagingSenderId': "800780596390",
  'appId': "1:800780596390:web:4c4029a1f7d91eb3333067",
  'measurementId': "G-19P192XXE0",
  'databaseURL': ""
}

firebase = initialize_app(firebase_config)

auth = firebase.auth() #auth for the user_token 


#------------------- Routing ------------------------


# def google_signin():

#     id_token = request.get('idToken')
    
#     #TODO: check whether the user is already in the database or not, if yes! take the user info and redirect using that to the homepage else create a new user in the database
    
#     try:
#         # Authenticate user with Google credential
#         user = auth.sign_in_with_google(id_token)
        
#         # Extract user information
#         uid = user['localId']
#         name = user['displayName']
#         email = user['email']
#         profile_image = user['photoURL']
#         print(list(email,name,profile_image))

#         # Store user data in database-----

#         #---------------------------------

#         return jsonify({'message': 'Google sign-in successful', 'uid': uid})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 401

@app.route('/sign-up', methods=['GET','POST'])
def signup():
    
    if request.method == 'POST':

        email = request.form.get('newemail')

        password = request.form.get('newpassword')

        name = request.form.get('name')

        user_type = request.form.get('radio')
        profile_image = ""

        try:

            print("in try block")
            
            user = auth.create_user_with_email_and_password(email, password)

            auth.update_profile(user["idToken"], display_name =  name)
            
            print("success\n",email,password,name,user_type)
            
            return(render_template('otp.html'))

            
           
            
        except Exception as e:
            
            message = json.loads(e.args[1])['error']['message']
            print(message)
            
            if message == "EMAIL_EXISTS":

                
                return render_template('signup.html', signup_error = "Email already exists. Login with you registered email or register with a new one.", signup_display_error = True)
            
            
            else:

                return render_template('signup.html', signup_error = "Something is not right. Please try again later or contact the administrator", signup_display_error = True)

            

    
    else:


        signup_error_message = "Something is not right. Please try again later or contact the administrator"
        return render_template('signup.html', signup_error = signup_error_message, signup_display_error = True)

@app.route('/login', methods=['GET','POST'])
def login():
    login_display_error = False
    print("login execution")

    if request.method == 'POST':
        try:
            print("entered try block")
            email = request.form.get('email')
            print(email)
            password = request.form.get('password')
            print(password)

            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            flash("login success")
            return redirect('/')
        
        except Exception as e:
                    print("Error during login:", e)  # Print error for debugging
                    login_error = "Invalid email or password. Please try again."
                    flash(login_error)
                    return render_template('signup.html', login_error=login_error, login_display_error=True)
        
    else:
        return render_template('signup.html')




@app.route('/logout')
def logout():

    session.pop('user', None)
    session.clear() 

    return redirect('/')

@app.route('/')
def homepage():
    tag = False #Make this tag True if you want to interact with the after login page for Development purpose
    
    if 'user' in session:

        #signed user
        
        user_id_token = session['user']["idToken"]
        try:
            auth.refresh(session['user']['refreshToken'])
            user = auth.get_account_info(user_id_token)['users'][0]
            email = user.get('email', '').split()[0]
            print(email)
            projects = [
                {
                    'name': 'Edge 24',
                    'description': 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Veniam deleniti eaque est error nam. Numquam magni voluptate laborum totam reprehenderit.',
                    'image_url': '/static/img/geek.jpg',
                    'link': '/static/img/1.png'  # Assuming this link is dynamic
                },
                {
                    'name': 'inspriIT',
                    'description': 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Veniam deleniti eaque est error nam. Numquam magni voluptate laborum totam reprehenderit.',
                    'image_url': '/static/img/geek.jpg',
                    'link': '/static/img/2.png'  # Assuming this link is dynamic
                }
                ,{
                    'name': 'Envisage',
                    'description': 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Veniam deleniti eaque est error nam. Numquam magni voluptate laborum totam reprehenderit.',
                    'image_url': '/static/img/Event posters.png',
                    'link': '/static/img/Envisage 24.png'  # Assuming this link is dynamic
                }
                ]
            return render_template('home.html',projects = projects)
        

        except KeyError as e:
            flash(e,"Something went wrong!")
    else:
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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/events')
def eventDashboard():
    return render_template('dashevent.html')

@app.route('/ticketVerification')
def eventticket():
    return render_template('qrscanner.html')

@app.route('/settings')
def eventsettings():
    return render_template('dashsetting.html')

@app.route('/venueBooking')
def venueBook():
    # Pass the list of clubs to the template
    clubs = ["GEEKONIX", "IIC", "SAMARTH"]
    colleges = ["TMSL"]
    venues = ["CONFERENCE HALL", "G-SERIES", "MAIN GROUND"]

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
    email_address = request.get('email_address')

    otp = generate_otp()
    otp_store[email_address] = otp  # Store OTP in memory

    send_email(email_address, otp)

    return jsonify({'message': 'OTP has been sent to {}'.format(email_address)})


@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    email_address = request.get('email_address')
    user_otp = request.get('otp')

    if email_address in otp_store and otp_store[email_address] == user_otp:
        del otp_store[email_address]  # Remove OTP from memory after successful verification
        return jsonify({'message': 'OTP verification successful'})
    else:
        return jsonify({'error': 'Invalid OTP'})
    

if __name__ == "__main__":
    app.run(debug=True)
    
