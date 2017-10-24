from flask import Flask, redirect, url_for, session, request, render_template_string
import requests
import os
import ast
import base64

#App config
ALLOWED_EXTENSIONS = set(['mp4'])

app = Flask(__name__)
app.secret_key = os.urandom(24)



@app.errorhandler(404)
def error_404(e):
    """
    - Displays the 404 error page.
    """
    error_page = ((requests.get(url='http://127.0.0.1:8080/html/{}'.format('404.html'))).content).decode("utf-8") # Done
    return render_template_string(error_page)



@app.route("/", methods = ['GET'])
def start(): #WORKS
    """
    - The starting page.
    - Redirects to login page if not logged in.
    - Redirects to dashboard if logged in.
    """
    logged_in = False
    if 'user' in session:
        logged_in = True
        is_admin = (requests.post(url='http://127.0.0.1:8080/is-admin', data={'username' : session['user']}).content).decode("utf-8") # Done
        if is_admin == "True":
            return redirect(url_for('dashboard'))
    most_viewed_video_IDs = ((requests.get('http://127.0.0.1:8080/get-most-viewed')).content).decode("utf-8") # Done
    most_viewed = {}
    most_viewed_video_IDs = ast.literal_eval(most_viewed_video_IDs)
    for ID in most_viewed_video_IDs:
        title = ((requests.get(url='http://127.0.0.1:8080/title/{}'.format(ID))).content).decode("utf-8") # Done
        views = ((requests.get(url='http://127.0.0.1:8080/views/{}'.format(ID))).content).decode("utf-8") # Done
        uploader = ((requests.get(url='http://127.0.0.1:8080/uploader/{}'.format(ID))).content).decode("utf-8") # Done
        details = [title, views, uploader]
        most_viewed.update({ID : details})
        homepage = ((requests.get(url='http://127.0.0.1:8080/html/{}'.format('homepage.html'))).content).decode("utf-8") # Done
    return render_template_string(homepage, logged_in = logged_in, most_viewed = most_viewed)



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
            return redirect(url_for("start"))
        else:
            login_page = ((requests.get(url='http://127.0.0.1:8080/html/{}'.format('login.html'))).content).decode("utf-8") # Done
            if login_error == False:
                return render_template_string(login_page)
            else:
                return render_template_string(login_page, loginError = True)
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
        is_valid_user = ((requests.post(url='http://127.0.0.1:8080/is-valid-user', data={'username' : username, 'password' : password})).content).decode("utf-8") # Done
        if is_valid_user == "True":
            session['user'] = username
            return redirect(url_for("start"))
        else:
            return redirect(url_for("login_form", l_error = True))



@app.route("/signup", methods = ['GET', 'POST'])
def signup_form(): #WORKS
    """
    In GET request
        - Displays sign up page.
    """
    if request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('start'))
        signup_error = request.args.get('s_error', False)
        signup_page = ((requests.get(url='http://127.0.0.1:8080/html/{}'.format('signup.html'))).content).decode("utf-8") # Done
        if signup_error == False:
            return render_template_string(signup_page)
        else:
            return render_template_string(signup_page, signupError = True)
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
        is_valid_username = ((requests.get(url='http://127.0.0.1:8080/is-valid-username/{}'.format(username))).content).decode("utf-8") # Done
        if is_valid_username == "False":
            requests.post(url='http://127.0.0.1:8080/add-user', data={'username' : username, 'password' : password}) # Done
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
        password_update_page = ((requests.get(url='http://127.0.0.1:8080/html/{}'.format('password_update.html'))).content).decode("utf-8") # Done
        if u_error == False:
            return render_template_string(password_update_page)
        else:
            return render_template_string(password_update_page, update_error = True)
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
        done = (requests.post(url='http://127.0.0.1:8080/update-password', data={'username' : username, 'old_password' : old_password, 'new_password' : new_password}).content).decode("utf-8") # Done
        if done == "True":
            return redirect(url_for('dashboard'))
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
        confirmation_page = ((requests.get(url='http://127.0.0.1:8080/html/{}'.format('delete-confirm.html'))).content).decode("utf-8") # Done
        if confirmation_error == False:
            return render_template_string(confirmation_page)
        else:
            return render_template_string(confirmation_page, c_error = True)
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
        is_deleted = ((requests.post(url='http://127.0.0.1:8080/delete-user', data={'username' : username, 'password' : password})).content).decode("utf-8") # Done
        if is_deleted == "True":
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
            is_admin = (requests.post(url='http://127.0.0.1:8080/is-admin', data={'username' : session['user']}).content).decode("utf-8") # Done
            if is_admin == "True":
                admin_dashboard = ((requests.get(url='http://127.0.0.1:8080/html/{}'.format('administrator_dashboard.html'))).content).decode("utf-8")
                return render_template_string(admin_dashboard, logged_in_username = session['user'])
            else:
                user_dashboard = ((requests.get(url='http://127.0.0.1:8080/html/{}'.format('user_dashboard.html'))).content).decode("utf-8")
                return render_template_string(user_dashboard, logged_in_username = session['user'])



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
        upload_page = ((requests.get(url='http://127.0.0.1:8080/html/{}'.format('upload.html'))).content).decode("utf-8")
        return render_template_string(upload_page)
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
        if file and allowed_file(file.filename):
            video_ID = ((requests.post(url='http://127.0.0.1:8080/upload', data={'username' : username, 'title' : title, 'file' : base64.b64encode(file.read())})).content).decode("utf-8") # Done
            return redirect(url_for('watch_video', v = video_ID))
        else:
            return redirect(url_for('upload_form'))




@app.route("/delete-video", methods = ['GET'])
def delete_own_video():
    """
    In GET request
        - Redirects to login page if not logged in.
        - If the uploader and current user are the same, it deletes the video.
        - Redirects to dashboard.
    """
    if 'user' not in session:
        return redirect(url_for('login_form'))
    video_ID = request.args.get('video_ID')
    uploader = ((requests.get('http://127.0.0.1:8080/uploader/{}'.format(video_ID))).content).decode("utf-8") # Done
    username = session['user']
    if username == uploader:
        pass
    return redirect(url_for('dashboard'))



@app.route("/watch", methods = ['GET'])
def watch_video(): #WORKS
    """
    In GET request
        - Plays the video with the corresponding video ID.
    """
    if request.method == 'GET':
        video_ID = request.args.get('v', None)
        if video_ID == None:
            return redirect(url_for('dashboard'))
        title = ((requests.get(url='http://127.0.0.1:8080/title/{}'.format(video_ID))).content).decode("utf-8") # Done
        uploader = ((requests.get(url='http://127.0.0.1:8080/uploader/{}'.format(video_ID))).content).decode("utf-8") # Done
        requests.post(url='http://127.0.0.1:8080/update-count', data={'video_ID' : video_ID})
        video_page = ((requests.get(url='http://127.0.0.1:8080/html/{}'.format('video.html'))).content).decode("utf-8")
        if 'user' in session:
            username = session['user']
            requests.post(url='http://127.0.0.1:8080/update-watched', data={'username' : username, 'video_ID' : video_ID})
            username = session['user']
            return render_template_string(video_page, video_ID = video_ID, title = title, uploader = uploader, logged_in = True)
        else:
            return render_template_string(video_page, video_ID = video_ID, title = title, uploader = uploader)



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
        results = ((requests.get(url='http://127.0.0.1:8080/fuzzy/{}'.format(search_key))).content).decode("utf-8") # Done
        result_dict = {}
        results = ast.literal_eval(results)
        logged_in = False
        if 'user' in session:
            logged_in = True
        for ID in results:
            title = ((requests.get(url='http://127.0.0.1:8080/title/{}'.format(ID))).content).decode("utf-8") # Done
            views = ((requests.get(url='http://127.0.0.1:8080/views/{}'.format(ID))).content).decode("utf-8") # Done
            uploader = ((requests.get(url='http://127.0.0.1:8080/uploader/{}'.format(ID))).content).decode("utf-8") # Done
            details = [title, views, uploader]
            result_dict.update({ID : details})
        search_page = ((requests.get(url='http://127.0.0.1:8080/html/{}'.format('search.html'))).content).decode("utf-8")
        return render_template_string(search_page, results = result_dict, search = search_key, logged_in = logged_in)



@app.route("/random", methods = ['GET'])
def random_video():
    """
    In GET request
        - Selects a random video from the database and redirects to the page of the video.
    """
    if request.method == 'GET':
        random_video_ID = ((requests.get(url='http://127.0.0.1:8080/random').content)).decode("utf-8") # Done
        return redirect(url_for('watch_video', v = random_video_ID))



@app.route("/watched", methods = ['GET'])
def watched_videos():
    """
    In GET request
        - Displays a page of all videos watched by the user in the WATCHED tables.
    """
    if 'user' not in session:
        return redirect(url_for('login_form'))
    username = session['user']
    watched_IDs = ((requests.get(url='http://127.0.0.1:8080/watched/{}'.format(username))).content).decode("utf-8") # Done
    watched_IDs = ast.literal_eval(watched_IDs)
    watched_dictionary = {}
    for ID in watched_IDs:
        title = ((requests.get(url='http://127.0.0.1:8080/title/{}'.format(ID))).content).decode("utf-8") # Done
        views = ((requests.get(url='http://127.0.0.1:8080/views/{}'.format(ID))).content).decode("utf-8") # Done
        uploader = ((requests.get(url='http://127.0.0.1:8080/uploader/{}'.format(ID))).content).decode("utf-8") # Done
        watched_dictionary.update({ID : [title, views, uploader]})
    watched_page = ((requests.get(url='http://127.0.0.1:8080/html/{}'.format('watched.html'))).content).decode("utf-8")
    return render_template_string(watched_page, watched = watched_dictionary)


#Admin part
@app.route("/adminsignup", methods = ['GET', 'POST'])
def admin_signup():
    """
    In GET request
	- Displays the signup page.
    """
    if request.method == 'GET':
    	if 'user' in session:
	    is_admin = (requests.post(url='http://127.0.0.1:8080/is-admin', data={'username' : session['user']}).content).decode("utf-8") 
	    if is_admin == "True":
		#return redirect(url_for('random_video'))
    	        #signup_error = request.args.get('s_error', False)
    		signup_page = ((requests.get(url='http://127.0.0.1:8080/html/{}'.format('adminsignup.html'))).content).decode("utf-8")
    		#if signup_error == "False":
        	return render_template_string(signup_page)
    		#else:
        	 #   return render_template_string(signup_page, signupError = True)
	    else:
		return redirect(url_for("dashboard"))
	else:
	    return redirect(url_for("start"))
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
        is_valid_username = ((requests.get(url='http://127.0.0.1:8080/is-valid-username/{}'.format(username))).content).decode("utf-8") # Done
        if is_valid_username == "False":
            requests.post(url='http://127.0.0.1:8080/add-admin', data={'username' : username, 'password' : password}) # Done
            session['user'] = username
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("signup_form", s_error = True))
    return ''

#List without Client-Server from old repo
@app.route("/admin-delete-video", methods = ['GET', 'POST']) #TEMPORARY
def admin_delete_video():
    """
    In GET request
	- Displays the list of videos
    """
    if request.method == 'GET':
	if 'user' in session:
	    is_admin = (requests.post(url="http://127.0.0.1:8080/is-admin", data = {'username' : session['user']}).content).decode("utf-8")
	    if is_admin == "True":
		#return redirect(url_for('random_video'))
		list_of_videos = {}
		list_of_videos = (requests.get(url="http://127.0.0.1:8080/list").content).decode("utf-8")
		list_html = (requests.get(url="http://127.0.0.1:8080/html/{}".format('list.html')).content).decode("utf-8")
		return render_template_string(list_html, lista = list_of_videos)
		#return render_template_string(list_of_videos)
    return ''	    	

@app.route("/admin-delete-user", methods = ['GET', 'POST'])
def admin_del_user():
    """
    In GET request
	- Displays the list of users.
    """
    if request.method == 'GET':
	if 'user' in session:
	   is_admin = (requests.post(url="http://127.0.0.1:8080/is-admin", data = {'username' : session['user']}).content).decode("utf-8")
	   if is_admin == "True":
		return ''	
    return ''		

if __name__ == "__main__":
    app.run(port=5000, threaded=True, debug=True)
