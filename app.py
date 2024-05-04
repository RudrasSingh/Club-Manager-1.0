from flask import *
from pyrebase import *
import database as db
from dotenv import load_dotenv
import os
from authlib.integrations.flask_client import OAuth
#-----------------setting up the app------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.secret_key = 'SECRET_KEY' #generate a secret key and use it here in this virtual env
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

#--------------Authlib---------------
oauth = OAuth(app)
oauth.register(
    "clubsync",
    client_id=os.getenv("OAUTH2_CLIENT_ID"),
    client_secret=os.getenv("OAUTH2_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email",},
    server_metadata_url=f'{os.getenv("OAUTH2_META_URL")}',
)
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
                
                flash("Account Created Successfully!","Success")
            return redirect('/')
        except Exception as e:
            print("Error During Signup:", e)
            return redirect('/sign-up')
              # Print error for debugging


    else:

        return render_template('signup.html')


@app.route("/signin-google")
def googleCallback():
    
    try:
        # fetch access token and id token using authorization code
        token = oauth.clubsync.authorize_access_token()
        # print(token,"\n\n",type(token))

        token = dict(token)
        print(json.dumps(token, indent = 4))
        # Extract necessary user data from the ID token
        personal = token.get('userinfo')
        user_info = {"name" : personal.get('name'),
                    "email" : personal.get('email'),
                    "id_token" : token.get('id_token')}

        # Set complete user information in the session
        print(user_info)
        session["user"] = user_info
        return redirect('/profile')
    except Exception as e:
        print("Error during google callback:", e)
        return redirect('/login')


@app.route("/google-login")
def googleLogin():
    try:
        if "user" in session:
            abort(404)
        return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))
    except Exception as e:
        flash("Error during google login:", "Failure")
        return redirect('/login')
    

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
    flash("Logged out successfully!","Success")
    return redirect('/')


@app.route('/forgot-password', methods=['GET','POST'])
def forgotPassword():
    if request.method == 'POST':
        try:
            email = request.form.get('user_email')
            try:
                auth.send_password_reset_email(email)
                flash("Password reset link sent to your email!","Success")
                return redirect('/login')
            except Exception as e:
                print("Error during password reset:", e)
                flash("Something went wrong!","Error")
                return redirect('/login')
            
        except Exception as e:

            print("Error during password reset:", e)
            flash("Something went wrong!","Error")
            return redirect('/login')
        
    return render_template('forgotPassword.html')


@app.route('/')
def homepage():
    """
    
    """   
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


@app.route('/verification')
def otp_verification():
    return render_template('otp.html')


@app.route('/dashboard')
def dashboard():
    try:    
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
    except Exception as e:
        print("Error during dashboard:", e)
        return redirect('/login')

@app.route('/profile')
def profile():
    return render_template('404.html')

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
    