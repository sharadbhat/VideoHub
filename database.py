import pymysql
import uuid
import os
import base64
from werkzeug.security import generate_password_hash, check_password_hash


class Database:
    def __init__(self): # WORKS
        self.db = pymysql.connect(host="localhost", user="root", passwd="******", db="video")
        self.cur = self.db.cursor()

    def is_valid_user(self, username, password): # WORKS
        """
        - Checks if the entered username and password corresponds to a valid user in the USERS and ADMINS table.
        """
        done = self.cur.execute("SELECT password FROM users WHERE username=\"{}\"".format(username))
        done2 = self.cur.execute("SELECT username FROM admins WHERE username=\"{}\"".format(username))
        if done == 0 and done2 == 0:
            return False
        else:
            if done == 1:
                self.cur.execute("SELECT password FROM users WHERE username=\"{}\"".format(username))
                stored_password = self.cur.fetchone()[0]
                return check_password_hash(stored_password, password)
            else:
                self.cur.execute("SELECT password FROM admins WHERE username=\"{}\"".format(username))
                stored_password = self.cur.fetchone()[0]
                return check_password_hash(stored_password, password)

    def is_valid_username(self, username):
        """
        - Checks if the username is already present in the USERS table.
        """
        done = self.cur.execute("SELECT username FROM users WHERE username=\"{}\"".format(username))
        done2 = self.cur.execute("SELECT username FROM admins WHERE username=\"{}\"".format(username))
        if done == 0 and done2 == 0:
            return False
        else:
            return True

    def is_admin(self, username): #WORKS
        """
        - Checks if a user is an admin in the ADMINS table..
        """
        done = self.cur.execute("SELECT username FROM admins WHERE username=\"{}\"".format(username))
        if done == 0:
            return False
        else:
            return True

    def add_user(self, username, password): #WORKS
        """
        - Add the new user credentials to the USERS table.
        """
        password_hash = generate_password_hash(password)
        try:
            self.cur.execute("INSERT INTO users VALUES(\"{}\", \"{}\")".format(username, password_hash))
            self.db.commit()
        except:
            self.db.rollback()

    def update_password(self, username, password): #WORKS
        """
        - Updates the password of the user in the USERS table.
        """
        password_hash = generate_password_hash(password)
        try:
            self.cur.execute("UPDATE users SET password = \"{}\" WHERE username = \"{}\"".format(password_hash, username))
            self.db.commit()
        except:
            self.db.rollback()

    def delete_user(self, username): #WORKS
        """
        - Deletes user credentials from the USERS table.
        """
        try:
            self.cur.execute("SELECT video_ID FROM videos WHERE uploader = \"{}\"".format(username))
            videos_to_delete = []
            for row in self.cur.fetchall():
                videos_to_delete.append(row[0])
            for ID in videos_to_delete:
                os.remove('static/videos/' + str(ID) + ".mp4")
            self.cur.execute("DELETE FROM users WHERE username = \"{}\"".format(username))
            self.db.commit()
        except:
            self.db.rollback()

    def upload_video(self, video_ID, username, title): #WORKS
        """
        - Updates VIDEOS table with video ID, uploader username and video title in the VIDEOS table.
        """
        try:
            self.cur.execute("INSERT INTO videos VALUES(\"{}\", \"{}\", \"{}\", 0, 0, 0)".format(video_ID, title, username))
            self.db.commit()
        except:
            self.db.rollback()

    def get_video_title(self, video_ID): #WORKS
        """
        - Returns the title of the video with the corresponding video ID from the VIDEOS table.
        """
        try:
            self.cur.execute("SELECT video_title FROM videos WHERE video_ID = \"{}\"".format(video_ID))
            title = self.cur.fetchone()[0]
            return title
        except:
            return "Error getting title"

    def update_view_count(self, video_ID): #WORKS
        """
        - Updates the view count for the corresponding video ID in the VIDEOS table.
        """
        try:
            self.cur.execute("UPDATE videos SET view_count = view_count + 1 WHERE video_ID = \"{}\"".format(video_ID))
            self.db.commit()
        except:
            self.db.rollback()

    def update_watched(self, username, video_ID): #WORKS
        """
        - Adds the username and video ID to the WATCHED table.
        """
        try:
            done = self.cur.execute("SELECT * FROM watched WHERE username = \"{}\" AND video_ID = \"{}\"".format(username, video_ID))
            if done == 0:
                self.cur.execute("INSERT INTO watched VALUES(\"{}\", \"{}\")".format(video_ID, username))
                self.db.commit()
        except:
            self.db.rollback()

    def get_video_uploader(self, video_ID): #WORKS
        """
        - Returns the username of the user that uploaded the video with the corresponding video ID.
        """
        try:
            done = self.cur.execute("SELECT uploader FROM videos WHERE video_ID = \"{}\"".format(video_ID))
            uploader = self.cur.fetchone()[0]
            return uploader
        except:
            return "Error getting username"
