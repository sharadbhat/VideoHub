from flask import Flask, render_template, redirect, url_for, session, request
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



@app.route("/", methods = ['GET'])
def start(): #WORKS
    """
    - The starting page.
    - Redirects to login page if not logged in.
    - Redirects to dashboard if logged in.
    """
    if 'user' in session:
        return redirect(url_for("dashboard"))
    else:
        most_viewed_video_IDs = db.get_most_viewed()
        most_viewed = {}
        for ID in most_viewed_video_IDs:
            title = db.get_video_title(ID)
            most_viewed.update({ID : title})
        return render_template('home.html', most_viewed = most_viewed)



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
    In GET request
        - Redirects to login page if not logged in.
        - Displays the password update form.
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
    In POST request
        - Gets the old and new passwords.
        - Checks the old password.
        - If it matches the stored password, password is updated.
        - Otherwise, error is thrown.
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



@app.route("/logout", methods = ['GET'])
def logout_user(): #WORKS
    """
    - Removes user from session.
    - Redirects to login page.
    """
    session.pop('user', None)
    return redirect(url_for("start"))



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



@app.route("/search", methods = ['POST'])
def search_videos():
    """
    In POST request
        - Accepts the search key from the user.
    """
    if request.method == 'POST':
        search_key = request.form['search']
        return redirect(url_for('results', search_query = search_key))



@app.route("/results", methods = ['GET'])
def results():
    """
    In GET request
        - Displays the search results.
    """
    if request.method == 'GET':
        search_key = request.args.get('search_query', None)
        if search_key == None:
            return redirect('dashboard')
        results = fuzzy(search_key)
        result_dict = {}
        for ID in results:
            result_dict.update({ID : db.get_video_title(ID)})
        return render_template('search.html', results = result_dict, search = search_key)



@app.route("/random", methods = ['GET'])
def random_video():
    """
    In GET request
        - Selects a random video from the database and redirects to the page of the video.
    """
    if request.method == 'GET':
        random_video_ID = db.get_random_ID()
        return redirect(url_for('watch_video', v = random_video_ID))



@app.route("/list") #TEMPORARY
def list():
    a = os.listdir('static/videos')
    result_dict = {}
    for ID in a:
        result_dict.update({ID : db.get_video_title(ID[:-4])})
    return render_template('list.html', lista = result_dict)

#Admin part

@app.route("/adminsignup", methods = ['GET', 'POST'])
def admin_signup_form(): #WORKS
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
            db.add_admin(username, password)
            session['user'] = username
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("signup_form", s_error = True))


if __name__ == "__main__":
    app.run(threaded=True)
