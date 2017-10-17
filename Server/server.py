from flask import Flask, request, send_file
import database
import base64
import os
import uuid
from fuzzy_search import fuzzy
from image_capture import save_image

app = Flask(__name__)
db = database.Database()

UPLOAD_FOLDER = 'static/videos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/html/<filename>", methods = ['GET'])
def return_html(filename):
    """
    - Returns the html file with the corresponding filename.
    """
    if request.method == 'GET':
        return send_file('./templates/{}'.format(filename), mimetype='text/html')



@app.route("/css/<filename>", methods = ['GET'])
def return_css(filename):
    """
    - Returns the css file with the corresponding filename.
    """
    if request.method == 'GET':
        return send_file('./static/css/{}'.format(filename), mimetype='text/css')



@app.route("/js/<filename>", methods = ['GET'])
def return_js(filename):
    """
    - Returns the js file with the corresponding filename.
    """
    if request.method == 'GET':
        return send_file('./static/js/{}'.format(filename), mimetype='text/js')



@app.route("/favicon.png", methods = ['GET'])
def return_favicon():
    """
    - Returns the favicon image.
    """
    if request.method == 'GET':
        return send_file('./static/img/favicon.png', mimetype='image/png')



@app.route("/is-available/<video_ID>", methods = ['GET'])
def return_availability(video_ID):
    """
    - Returns True is the video ID is present in the database.
    - Otherwise False.
    """
    if request.method == 'GET':
        return str(db.is_available(video_ID))



@app.route("/video/<video_ID>", methods = ['GET'])
def return_video(video_ID):
    """
    - Returns the video file with the corresponding video ID.
    """
    if request.method == 'GET':
        return send_file('./static/videos/{}.mp4'.format(video_ID), mimetype='video/mp4')



@app.route("/image/<video_ID>", methods = ['GET'])
def return_image(video_ID):
    """
    - Returns the image file with the corresponding video ID.
    """
    if request.method == 'GET':
        return send_file('./static/images/{}.jpg'.format(video_ID), mimetype='image/jpg')



@app.route("/title/<video_ID>", methods = ['GET'])
def return_title(video_ID):
    """
    - Returns the title of the video with the corresponding video ID.
    """
    if request.method == 'GET':
        return db.get_video_title(video_ID)



@app.route("/views/<video_ID>", methods = ['GET'])
def return_views(video_ID):
    """
    - Returns the view count of the video with the corresponding video ID.
    """
    if request.method == 'GET':
        return db.get_views(video_ID)



@app.route("/uploader/<video_ID>", methods = ['GET'])
def return_uploader(video_ID):
    """
    - Returns the uploader of the video with the corresponding video ID.
    """
    if request.method == 'GET':
        return db.get_video_uploader(video_ID)



@app.route("/update-count", methods = ['POST'])
def update_count():
    """
    - Updates the view count of the video with the corresponding video ID.
    """
    if request.method == 'POST':
        video_ID = request.form['video_ID']
        db.update_view_count(video_ID)
        return "1"



@app.route("/update-watched", methods = ['POST'])
def update_watched():
    """
    - Updates the watched list of the user.
    """
    if request.method == 'POST':
        username = request.form['username']
        video_ID = request.form['video_ID']
        db.update_watched(username, video_ID)
        return "1"



@app.route("/random", methods = ['GET'])
def return_random_ID():
    """
    - Return a ranodm video ID.
    """
    if request.method == 'GET':
        return db.get_random_ID()



@app.route("/fuzzy/<search_key>", methods = ['GET'])
def fuzzy_results(search_key):
    """
    - Returns a list of closest matches for the search key.
    """
    if request.method == 'GET':
        return str(fuzzy(search_key))



@app.route("/get-most-viewed", methods = ['GET'])
def return_most_viewed():
    """
    - Returns a list of most viewed videos.
    """
    if request.method == 'GET':
        return str(db.get_most_viewed())



@app.route("/is-valid-user", methods = ['POST'])
def return_is_valid_user():
    """
    - Returns True if the user is a valid user.
    - Else returns False.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return str(db.is_valid_user(username, password))



@app.route("/is-valid-username/<username>", methods = ["GET"])
def return_is_valid_username(username):
    if request.method == 'GET':
        return str(db.is_valid_username(username))



@app.route("/add-user", methods = ['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db.add_user(username, password)
        return "1"



@app.route("/update-password", methods = ['POST'])
def update_password():
    if request.method == 'POST':
        username = request.form['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        if db.is_valid_user(username, old_password) == True:
            db.update_password(username, new_password)
            return "True"
        else:
            return "False"



@app.route("/delete-user", methods = ['POST'])
def delete_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.is_valid_user(username, password):
            db.delete_user(username)
            return "True"
        else:
            return "False"



@app.route("/is-admin", methods = ['POST'])
def return_is_admin():
    if request.method == 'POST':
        username = request.form['username']
        return str(db.is_admin(username))



@app.route("/upload", methods = ['POST'])
def upload_video():
    if request.method == 'POST':
        video_ID = str(base64.b64encode(str.encode(str(uuid.uuid4().fields[5]))))[2:-1]
        username = request.form['username']
        title = request.form['title']
        file = request.form['file']
        filename = open('./static/videos/{}.mp4'.format(video_ID), "wb")
        filename.write(base64.b64decode(file))
        db.upload_video(video_ID, username, title)
        save_image(video_ID)
        return video_ID



@app.route("/watched/<username>", methods = ['GET'])
def return_watched(username):
    if request.method == 'GET':
        return str(db.get_watched(username))



@app.route("/uploaded/<username>", methods = ['GET'])
def return_uploaded(username):
    if request.method == 'GET':
        return str(db.get_uploaded(username))



@app.route("/is-user-present/<username>", methods = ['GET'])
def return_user_availability(username):
    if request.method == 'GET':
        return str(db.is_user_present(username))



@app.route("/delete-video", methods = ['POST'])
def delete_video():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        video_ID = request.form['video_ID']
        if db.is_valid_user(username, password) == True:
            db.delete_video(video_ID)
            return str(True)
        else:
            return str(False)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
