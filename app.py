from flask import *
from pyrebase import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random 
import database as db
from dotenv import load_dotenv
import os
from datetime import timedelta
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
    db.connect_to_database()

@app.after_request
def after_request(response):
    # Close database connection after each request
    db.close_connection()
    return response

#--------------session Handling---------------

# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
# app.permanent_session_lifetime = timedelta(days=31)



#------------------------firebase setting---------------------------

firebase_config = {
  'apiKey': os.getenv('APIKEY'),
  'authDomain': os.getenv('AUTHDOMAIN'),
  'projectId': os.getenv('PROJECTID'),
  'storageBucket': os.getenv('STORAGEBUCKET'),
  'messagingSenderId': os.getenv('MESSAGINGSENDERID'),
  'appId': os.getenv('APPID'),
  'measurementId': os.getenv('MEASUREMENTID'),
  'databaseURL': ""
}

firebase = initialize_app(firebase_config)
auth = firebase.auth() #auth for the user_token 

#------------------- Routing ------------------------

@app.route('/sign-up', methods=['GET','POST'])
def signup():
    
    if request.method == 'POST':

        email = request.form.get('newemail')
        password = request.form.get('newpassword')
        name = request.form.get('name')
        user_type = request.form.get('radio')

        try:
            user = auth.create_user_with_email_and_password(email, password)
            
            if user_type.lower() == 'club':
                session["user"] = user
                print(user)
                db.create_club(email,name)
                flash("Account Created Successfully!","Success")
            return redirect('/')
        except Exception as e:
            print("Error During Signup:", e)  # Print error for debugging


    else:
        signup_error_message = "Something is not right. Please try again later or contact the administrator"
        return render_template('signup.html', signup_error = signup_error_message, signup_display_error = True)


@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')

            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
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
            return render_template('home.html', projects = projects)
        

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
        
    user = session.get('user')
    print(user)
    email = user.get('email', '').split()[0]
    print(email)
    context = db.fetch_clubs(email)
    clubName = ""
    for i in context:
        if i[1] == email:
            context = i[0]
    
    
    return render_template('dashboard.html',context = context)

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


if __name__ == "__main__":
    app.run(debug=True)
    