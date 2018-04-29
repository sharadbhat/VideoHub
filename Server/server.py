from flask import Flask, request, send_file
import database
import base64
import os
import uuid
import calendar
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



@app.route("/upload-date/<video_ID>", methods = ['GET'])
def return_date(video_ID):
    """
    - Returns the upload date of the video with the corresponding video ID.
    """
    if request.method == 'GET':
        upload_date = str(db.get_upload_date(video_ID))
        vid_date = upload_date.split("-")
        month = calendar.month_abbr[int(vid_date[1])]
        video_upload_date = "{} {}, {}".format(month, vid_date[2], vid_date[0])
        return video_upload_date



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
        video_dict, video_titles = db.video_dict()
        return str(fuzzy(search_key, video_dict, video_titles))



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
    """
    - Checks if the user is a valid user.
    """
    if request.method == 'GET':
        return str(db.is_valid_username(username))



@app.route("/add-user", methods = ['POST'])
def add_user():
    """
    - Adds the new user credentials to the database.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db.add_user(username, password)
        return "1"



@app.route("/update-password", methods = ['POST'])
def update_password():
    """
    - Updates the password of the user.
    """
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
    """
    - Deletes the user's account.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.is_valid_user(username, password):
            db.delete_user(username)
            return "True"
        else:
            return "False"



@app.route("/is-admin/<username>", methods = ['GET'])
def return_is_admin(username):
    """
    - Checks if the user is an administrator.
    """
    if request.method == 'GET':
        return str(db.is_admin(username))



@app.route("/upload", methods = ['POST'])
def upload_video():
    """
    - Uploads the video.
    """
    if request.method == 'POST':
        video_ID = str(base64.urlsafe_b64encode(str.encode(str(uuid.uuid4().fields[5]))))[2:-1]
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
    """
    - Returns a list of video IDs watched by the user.
    """
    if request.method == 'GET':
        return str(db.get_watched(username))



@app.route("/uploaded/<username>", methods = ['GET'])
def return_uploaded(username):
    """
    - Returns a list of video IDs uploaded by the user.
    """
    if request.method == 'GET':
        return str(db.get_uploaded(username))



@app.route("/is-user-present/<username>", methods = ['GET'])
def return_user_availability(username):
    """
    - Checks if the user is present in the database.
    """
    if request.method == 'GET':
        return str(db.is_user_present(username))



@app.route("/delete-video", methods = ['POST'])
def delete_video():
    """
    - If the user is the uploader of the video, it is deleted.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        video_ID = request.form['video_ID']
        if db.is_valid_user(username, password) == True:
            db.delete_video(video_ID)
            return str(True)
        else:
            return str(False)



@app.route("/get-random/<video_ID>", methods = ['GET'])
def return_random_video_IDs(video_ID):
    """
    - Returns 5 random video IDs.
    - If the list contains the current video ID, it is removed.
    """
    if request.method == 'GET':
        random = db.get_five_random_IDs()
        if video_ID in random:
            random.remove(video_ID)
        return str(random)



@app.route("/flag", methods = ['POST'])
def flag_video_ID():
    """
    - Gets the username and the video ID to be flagged.
    - Flags the video is the FLAGS table.
    """
    if request.method == 'POST':
        username = request.form['username']
        video_ID = request.form['video_ID']
        db.flag_ID(username, video_ID)
        return "1"



@app.route("/user-video-count/<username>", methods = ['GET'])
def return_user_video_count(username):
    """
    In GET request
        - Returns number of videos uploaded by the user.
    """
    if request.method == 'GET':
        return str(db.get_user_video_count(username))



@app.route("/user-view-count/<username>", methods = ['GET'])
def return_user_view_count(username):
    """
    In GET request
        - Returns number of views on all videos uploaded by the user.
    """
    if request.method == 'GET':
        return str(db.get_user_view_count(username))


@app.route("/user-best-video/<username>", methods = ['GET'])
def return_user_best_video(username):
    """
    In GET request
        - Returns video ID of the video uploaded by the user with the highest view count.
    """
    if request.method == 'GET':
        return str(db.get_best_video_ID(username))



@app.route("/user-fav-video/<username>", methods = ['GET'])
def return_user_fav_video(username):
    """
    In GET request
        - Returns video ID of the video uploaded by the user with the highest view count.
    """
    if request.method == 'GET':
        return str(db.get_fav_video_ID(username))



# ADMIN PART

@app.route("/add-admin", methods = ['POST'])
def add_admin():
    """
    In POST request
        - Adds the new administrator to the ADMINS table.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db.add_admin(username, password)
        return "1"



@app.route("/flagger/<video_ID>", methods = ['GET'])
def return_flagger(video_ID):
    """
    In GET request
        - Returns the username of the user that flagged the video with the corresponding video ID from the FLAGS table.
    """
    if request.method == 'GET':
        return str(db.get_flagger(video_ID))



@app.route("/flagged", methods = ['GET'])
def return_flagged():
    """
    In GET request
        - Returns a list of flagged videos.
    """
    if request.method == 'GET':
        return str(db.get_flagged())



@app.route("/admin-delete-video", methods = ['POST'])
def admin_delete_video():
    """
    In POST request
        - Deletes the video from VIDEOS table.
    """
    if request.method == 'POST':
        video_ID = request.form['video_ID']
        print(video_ID)
        db.delete_video(video_ID)
        return "1"



@app.route("/user-list", methods = ['GET'])
def return_users_list():
    """
    In GET request
        - Returns a list of users in the database.
    """
    if request.method == 'GET':
        return str(db.user_list())



@app.route("/num-videos/<username>", methods = ['GET'])
def return_user_video_number(username):
    """
    In GET request
        - Returns the number of videos uploaded by the user with the corresponding username.
    """
    if request.method == 'GET':
        return str(db.get_video_num(username))



@app.route("/num-flags/<username>", methods = ['GET'])
def return_user_flagged_number(username):
    """
    In GET request
        - Returns the number of videos uploaded by the user that have been flagged by other users.
    """
    if request.method == 'GET':
        return str(db.get_flagged_num(username))



@app.route("/admin-delete-user", methods = ['POST'])
def admin_delete_user():
    """
    In POST request
        - Delete the user with the corresponding username.
    """
    if request.method == 'POST':
        username = request.form['username']
        db.delete_user(username)
        return "1"



@app.route("/user-count", methods = ['GET'])
def return_user_count():
    """
    In GET request
        - Returns number of users in the USERS table.
    """
    if request.method == 'GET':
        return str(db.get_user_count())



@app.route("/video-count", methods = ['GET'])
def return_video_count():
    """
    In GET request
        - Returns number of videos in the VIDEOS table.
    """
    if request.method == 'GET':
        return str(db.get_video_count())



@app.route("/view-count", methods = ['GET'])
def return_view_count():
    """
    In GET request
        - Returns number of views on all videos in the VIDEOS table.
    """
    if request.method == 'GET':
        return str(db.get_total_view_count())



@app.route("/flag-count", methods = ['GET'])
def return_flag_count():
    """
    In GET request
        - Returns number of flagged videos in the VIDEOS table.
    """
    if request.method == 'GET':
        return str(db.get_flag_count())



@app.route("/favourites/<username>", methods = ['GET'])
def return_favourites(username):
    """
    In GET request
        - Returns a list of videos favourited by the user.
    """
    if request.method == 'GET':
        return str(db.get_favourites(username))



@app.route("/remove-flag", methods = ['POST'])
def remove_flag():
    """
    In POST request
        - Removes the flag for the video with the corresponding video ID from the FLAGS table.
    """
    if request.method == 'POST':
        video_ID = request.form['video_ID']
        db.delete_flag(video_ID)
        return "1"




if __name__ == '__main__':
    app.run(port=8080, debug=True)
