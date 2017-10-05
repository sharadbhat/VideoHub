from flask import Flask, render_template, redirect, url_for, session, request
from werkzeug import secure_filename
import os
import database

#App config
UPLOAD_FOLDER = 'videos'
ALLOWED_EXTENSIONS = set(['mp4'])

DEBUG = True
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = database.Database()



@app.route("/")
def start():
    """
    - The starting page.
    - Redirects to login page if not logged in.
    - Redirects to dashboard if logged in.
    """
    if 'user' in session:
        return redirect(url_for("dashboard"), username = session['user'])
    else:
        return redirect(url_for("login_form"))



@app.route("/login", methods = ['POST', 'GET'])
def login_form():
    """
    In GET request,
        - Redirects to dashboard if logged in.
        - Displays login form if not logged in.
    """
    if request.method == 'GET':
        login_error = request.args.get('l_error', False)
        if 'user' in session:
            return redirect(url_for("dashboard"))
        else:
            if login_error == False:
                return render_template('login.html')
            else:
                return render_template('login.html', loginError = "Invalid credentials")
    """
    In POST request
        - Gets data from form.
        - Validates user credentials.
    """
    if request.method == 'POST':
        username = (request.form['username']).lower().strip()
        password = (request.form['password'])
        if db.is_valid_user(username, password) == True:
            session['user'] = username
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("login_form", l_error = True))



@app.route("/signup", methods = ['GET', 'POST'])
def signup_form():
    """
    In GET request
        - Displays sign up page.
    """
    if request.method == 'GET':
        signup_error = request.args.get('s_error', False)
        if signup_error == False:
            return render_template('signup.html')
        else:
            return render_template('signup.html', signupError = "Username already present")
    """
    In POST request
        - Gets data from form.
        - Checks if username is not already present.
        - Adds to database if not present.
        - Redirects to dashboard.
    """
    if request.method == 'POST':
        username = (request.form['username']).lower().strip()
        password = (request.form['password'])
        if db.is_valid_username(username) == False:
            db.add_user(username, password)
            session['user'] = username
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("signup_form", s_error = True))


@app.route("/dashboard", methods = ['GET'])
def dashboard():
    """
    - Redirects to login page if not logged in.
    - Displays dashboard page if logged in.
    """
    if request.method == 'GET':
        if 'user' not in session:
            return redirect(url_for("login_form"))
        else:
            if db.is_admin(session['user']):
                return render_template('administrator_dashboard.html', logged_in_username = session['user'])
            else:
                return render_template('user_dashboard.html', logged_in_username = session['user'])



def allowed_file(filename):
    """
    - Checks if the uploaded file is an MP4 file.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/upload", methods = ['GET', 'POST'])
def upload_form():
    """
    In GET request
        - Displays upload form.
    """
    if request.method == 'GET':
        if 'user' not in session:
            return redirect(url_for('login_form'))
        return render_template('upload.html')
    """
    In POST request
        - Accepts video from user.
    """
    if request.method == 'POST':
        file = request.files['file']
        username = session['user']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('upload_form'))



@app.route("/delete")
def delete_own_account():
    """
    - Deletes the user credentials from the database.
    - Redirects to login page.
    """
    username = session['user']
    db.delete_user(username)
    session.pop('user', None)
    return redirect(url_for("login_form"))



@app.route("/logout")
def logout():
    """
    - Removes user from session.
    - Redirects to login page.
    """
    session.pop('user', None)
    return redirect(url_for("login_form"))





if __name__ == "__main__":
    app.run(threaded=True)
