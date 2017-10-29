import pymysql
import uuid
import os
import base64
from werkzeug.security import generate_password_hash, check_password_hash


class Database:
    def __init__(self): # WORKS
        self.db = pymysql.connect(host="localhost", user="root", passwd="citi69bank", db="video")
        self.cur = self.db.cursor()

    def get_most_viewed(self):
        """
        - Returns a list of top 10 video IDs in the descending order of view count from the VIDEOS table.
        """
        self.cur.execute("SELECT video_ID FROM videos ORDER BY CAST(view_count as decimal) DESC LIMIT 10")
        most_viewed_video_IDs = []
        for ID in self.cur.fetchall():
            most_viewed_video_IDs.append(ID[0])
        return most_viewed_video_IDs

    def is_valid_user(self, username, password): # WORKS
        """
        - Checks if the entered username and password corresponds to a valid user in the USERS and ADMINS table.
        """
        done1 = self.cur.execute("SELECT password FROM users WHERE username=\"{}\"".format(username))
        done2 = self.cur.execute("SELECT username FROM admins WHERE username=\"{}\"".format(username))
        if done1 == 0 and done2 == 0: # If both queries are unsuccessful, username doesn't exist in both tables.
            return False
        else:
            if done1 == 1: # If username exists in USERS table.
                self.cur.execute("SELECT password FROM users WHERE username=\"{}\"".format(username))
                stored_password = self.cur.fetchone()[0]
                return check_password_hash(stored_password, password) # Returns True if the hashes match.
            else: # If username exists in ADMINS table.
                self.cur.execute("SELECT password FROM admins WHERE username=\"{}\"".format(username))
                stored_password = self.cur.fetchone()[0]
                return check_password_hash(stored_password, password) # Returns True if the hashes match.

    def is_valid_username(self, username):
        """
        - Checks if the username is already present in the USERS table.
        """
        done1 = self.cur.execute("SELECT username FROM users WHERE username=\"{}\"".format(username))
        done2 = self.cur.execute("SELECT username FROM admins WHERE username=\"{}\"".format(username))
        if done1 == 0 and done2 == 0: # If both queries are unsuccessful, username doesn't exist in both tables.
            return False
        else:
            return True

    def is_admin(self, username): #WORKS
        """
        - Checks if a user is an admin in the ADMINS table..
        """
        done = self.cur.execute("SELECT username FROM admins WHERE username=\"{}\"".format(username))
        if done == 0: # If query is unsuccessful, username is not an administrator.
            return False
        else:
            return True

    def add_user(self, username, password): #WORKS
        """
        - Add the new user credentials to the USERS table.
        """
        password_hash = generate_password_hash(password) # Generates a SHA256 hash.
        try:
            self.cur.execute("INSERT INTO admins VALUES(\"{}\", \"{}\")".format(username, password_hash))
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
                videos_to_delete.append(row[0]) # Get video IDs of all videos uploaded by the user.
            for ID in videos_to_delete:
                os.remove('static/videos/' + str(ID) + '.mp4') # Deletes the video from the static/videos directory.
                os.remove('static/images/' + str(ID) + '.jpg') # Deletes the image from the static/images directory.
            self.cur.execute("DELETE FROM users WHERE username = \"{}\"".format(username))
            self.db.commit()
        except:
            self.db.rollback()

    def upload_video(self, video_ID, username, title): #WORKS
        """
        - Updates VIDEOS table with video ID, uploader username and video title in the VIDEOS table.
        """
        try:
            view_count = 0
            upvotes = 0
            downvotes = 0
            self.cur.execute("INSERT INTO videos VALUES(\"{}\", \"{}\", \"{}\", {}, {}, {})".format(video_ID, title, username, view_count, upvotes, downvotes))
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
            self.cur.execute("UPDATE videos SET view_count = view_count + 1 WHERE video_ID = \"{}\"".format(video_ID)) # Adds 1 to the existing value.
            self.db.commit()
        except:
            self.db.rollback()

    def update_watched(self, username, video_ID): #WORKS
        """
        - Adds the username and video ID to the WATCHED table.
        """
        try:
            done = self.cur.execute("SELECT * FROM watched WHERE username = \"{}\" AND video_ID = \"{}\"".format(username, video_ID))
            if done == 0: # If the query was unsuccessful, row does not exist.
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

    def get_random_ID(self):
        """
        - Returns a random video ID from the VIDEOS table.
        """
        self.cur.execute("SELECT video_ID FROM videos ORDER BY RAND() LIMIT 1") # Selects video_ID from 1 random row.
        return self.cur.fetchone()[0]

    def get_watched(self, username):
        """
        - Returns a list of video IDs watched by the user from the WATCHED table.
        """
        self.cur.execute("SELECT video_ID FROM watched WHERE username = \"{}\"".format(username))
        watched_video_IDs = []
        for ID in self.cur.fetchall():
            watched_video_IDs.append(ID[0])
        return watched_video_IDs

    def get_views(self, video_ID):
        """
        - Returns the view count of the video with the corresponding video_ID.
        """
        self.cur.execute("SELECT view_count FROM videos WHERE video_ID = \"{}\"".format(video_ID))
        return self.cur.fetchone()[0]

    def delete_video(self, video_ID):
        """
        - Deletes the video from the database.
        """
        try:
            self.cur.execute("DELETE FROM videos WHERE video_ID = \"{}\"".format(video_ID))
            self.db.commit()
            os.remove('static/videos/' + str(video_ID) + '.mp4')
            os.remove('static/images/' + str(video_ID) + '.jpg')
        except:
            self.db.rollback()

#Admin part
    def add_admin(self, username, password):
	"""
        - Adds the new admin credentials to the ADMINS table.
        """
        password_hash = generate_password_hash(password) # Generates a SHA256 hash.
        try:
            self.cur.execute("INSERT INTO admins VALUES(\"{}\", \"{}\")".format(username, password_hash))
            self.db.commit()
        except:
            self.db.rollback()

    def list_of_users(self):
	"""
	- Returns the list of all users in the USERS table.
	"""
	self.cur.execute("Select username from users")
	usernames = []	
	for name in self.cur.fetchall():
	    usernames.append(name[0])
	return usernames

    def list_of_flagged(self):
	"""
	- Returns the list of all the flagged videos.
	"""
	self.cur.execute("Select video_ID from flags")
	flagged_videos = []
	for video in self.cur.fetchall():
	    flagged_videos.append(video[0])
	return flagged_videos




