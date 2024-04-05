from flask import *
from pyrebase import *
from time import sleep
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
    return redirect('home.html') #changed the index.html to home.html

#for the dynamic events part

@app.route('/')
def index():
    # Data that you want to pass to the template
    projects = [
        {
            'name': 'ENVISAGE',
            'description': 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Veniam deleniti eaque est error nam. Numquam magni voluptate laborum totam reprehenderit.',
            'image_url': '/src/jpg/Event posters (1).png',
            'link': '/static/envi_logo.png'  # Assuming this link is dynamic
        }
        # Add more projects as needed
    ]
    return render_template('home.html', projects=projects)




if __name__ == "__main__":
    app.run(debug=True)
    

