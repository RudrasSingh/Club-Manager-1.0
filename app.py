from flask import *
from pyrebase import *
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

@app.route('/login')
def signupPage():
    return render_template('signup.html')

@app.route('/verification')
def otp_verification():
    return render_template('otp.html')

def homepage():
    return redirect('index.html')

@app.route('/home')
def signupPage():
    return render_template('') #home page link to be added 

@app.route('/about')
def signupPage():
    return render_template('')  #about page link to be added

@app.route('/upcoming_events')
def signupPage():
    return render_template('')  #upcoming events page link to be added 

@app.route('/team')
def signupPage():
    return render_template('')  #team page link to be added 

@app.route('/upcoming_events')
def signupPage():
    return render_template('')  #upcoming events page link to be added 

if __name__ == "__main__":
    app.run(debug=True)
    

