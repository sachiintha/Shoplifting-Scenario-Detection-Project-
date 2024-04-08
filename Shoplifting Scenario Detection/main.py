from flask import Flask, render_template, Response, request, redirect, url_for
import pyrebase
import camera

app = Flask(__name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera.VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



# Firebase configuration
config = {
    "apiKey": "AIzaSyCa-eq2enXsxV1iSXne44k8GNpm4T15cqc",
    "authDomain": "facial-expression-105de.firebaseapp.com",
    "projectId": "facial-expression-105de",
    "storageBucket": "facial-expression-105de.appspot.com",
    "messagingSenderId": "23346404897",
    "appId": "1:23346404897:web:be90d6b4b5cc2b91dd4d60",
    "measurementId": "G-E13KF0WFT8",
    "databaseURL": "https://facial-expression-105de-default-rtdb.firebaseio.com/"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/shoplifting_detected')
def shoplifting_detected():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        # Redirect to shoplifting detected page on successful login
        return redirect(url_for('shoplifting_detected'))
    except Exception as e:
        return "Login failed: " + str(e)

if __name__ == '__main__':
    app.run(debug=True)
