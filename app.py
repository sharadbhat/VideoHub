from flask import Flask, render_template, redirect, url_for, session, request, send_from_directory
from werkzeug import secure_filename
import os
from fuzzy_search import fuzzy
import base64
import uuid
import database

#App config
UPLOAD_FOLDER = 'static/videos'
ALLOWED_EXTENSIONS = set(['mp4'])

DEBUG = True
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = database.Database()



@app.route("/")
def start(): #WORKS
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
def login_form(): #WORKS
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
                return render_template('login.html', loginError = True)
    """
    In POST request
        - Gets data from form.
        - Validates user credentials.
    """
    if request.method == 'POST':
        if 'user' in session:
            return redirect(url_for('dashboard'))
        username = (request.form['username']).lower().strip()
        password = (request.form['password'])
        if db.is_valid_user(username, password) == True:
            session['user'] = username
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("login_form", l_error = True))



@app.route("/signup", methods = ['GET', 'POST'])
def signup_form(): #WORKS
    """
    In GET request
        - Displays sign up page.
    """
    if request.method == 'GET':
        signup_error = request.args.get('s_error', False)
        if signup_error == False:
            return render_template('signup.html')
        else:
            return render_template('signup.html', signupError = True)
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



@app.route("/change-password", methods = ['GET', 'POST'])
def password_update_form(): #WORKS
    """
    """
    if request.method == 'GET':
        u_error = request.args.get('u_error', False)
        if 'user' not in session:
            return redirect(url_for('login_form'))
        if u_error == False:
            return render_template('password_update.html')
        else:
            return render_template('password_update.html', update_error = True)
    """
    """
    if request.method == 'POST':
        if 'user' not in session:
            return redirect(url_for('login_form'))
        username = session['user']
        old_password = request.form['oldPassword']
        new_password = request.form['newPassword']
        if db.is_valid_user(username, old_password) == True:
            db.update_password(username, new_password)
            return redirect(url_for('dashboard', message = 'Password updated'))
        else:
            return redirect(url_for('password_update_form', u_error = True))


@app.route("/delete", methods = ['GET', 'POST'])
def delete_own_account(): #WORKS
    """
    In GET request
        - Displays confirmation page.
    """
    if request.method == 'GET':
        if 'user' not in session:
            return redirect(url_for('login_form'))
        confirmation_error = request.args.get('c_error', False)
        if confirmation_error == False:
            return render_template('delete-confirm.html')
        else:
            return render_template('delete-confirm.html', c_error = True)
    """
    In POST request
        - Deletes the user credentials from the database.
        - Redirects to login page.
    """
    if request.method == 'POST':
        if 'user' not in session:
            return redirect(url_for('login_form'))
        username = session['user']
        password = request.form['password']
        if db.is_valid_user(username, password) == True:
            db.delete_user(username)
            session.pop('user', None)
            return redirect(url_for("login_form"))
        else:
            return redirect(url_for('delete_own_account', c_error = True))



@app.route("/logout")
def logout_user(): #WORKS
    """
    - Removes user from session.
    - Redirects to login page.
    """
    session.pop('user', None)
    return redirect(url_for("login_form"))



@app.route("/dashboard", methods = ['GET'])
def dashboard(): #WORKS
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



def allowed_file(filename): #WORKS
    """
    - Checks if the uploaded file is an MP4 file.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/upload", methods = ['GET', 'POST'])
def upload_form(): #WORKS
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
        if 'user' not in session:
            return redirect(url_for('login_form'))
        file = request.files['file']
        username = session['user']
        title = request.form['title']
        video_ID = str(base64.b64encode(str.encode(str(uuid.uuid4().fields[5]))))[2:-1]
        if file and allowed_file(file.filename):
            db.upload_video(video_ID, username, title)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_ID + ".mp4"))
            return redirect(url_for('watch_video', v = video_ID))
        else:
            return redirect(url_for('upload_form'))



@app.route("/watch", methods = ['GET'])
def watch_video(): #WORKS
    """
    In GET request
        - Plays the video with the corresponding video ID.
    """
    if request.method == 'GET':
        video_ID = request.args.get('v', None)
        title = db.get_video_title(video_ID)
        uploader = db.get_video_uploader(video_ID)
        if video_ID == None:
            return redirect(url_for('dashboard'))
        db.update_view_count(video_ID)
        if 'user' in session:
            username = session['user']
            db.update_watched(username, video_ID)
            return render_template('video.html', video_ID = video_ID, title = title, uploader = uploader, username = session['user'])
        else:
            return render_template('video.html', video_ID = video_ID, title = title, uploader = uploader)



@app.route("/search")
def search_videos():
    """
    In GET request
        - Displays the search results.
    """
    if request.method == 'GET':
        search_key = request.args.get('search', None)
        if search_key == None:
            return redirect('dashboard')
        results = fuzzy(search_key)
        return render_template('search.html', results = results)



@app.route("/list") #TEMPORARY
def list():
    a = os.listdir('static/videos')
    return render_template('list.html', lista = a)


if __name__ == "__main__":
    app.run(threaded=True)
