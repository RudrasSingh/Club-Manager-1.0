from flask import *

app = Flask(__name__)

@app.route('/')
def landingPage():
    return render_template('signup.html')

@app.route('/homepage')
def signupPage():
    return render_template()



if __name__ == "__main__":

    app.run(debug=True)
    
