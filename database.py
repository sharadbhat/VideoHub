import pymysql
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


class Database:
    def __init__(self): # WORKS
        self.db = pymysql.connect(host="localhost", user="root", passwd="shamanmb", db="video")
        self.cur = self.db.cursor()

    def is_valid_user(self, username, password): # WORKS
        """
        - Checks if the entered username and password corresponds to a valid user in the USERS table.
        """
        done = self.cur.execute("SELECT password FROM users WHERE username=\"{}\"".format(username))
        done2 = self.cur.execute("SELECT username FROM admins WHERE username=\"{}\"".format(username))
        if done == 0 and done2 == 0:
            return False
        else:
            if done == 1:
                self.cur.execute("SELECT password FROM users WHERE username=\"{}\"".format(username))
                stored_password = self.cur.fetchone()[0]
                is_valid = check_password_hash(stored_password, password)
                return is_valid
            else:
                self.cur.execute("SELECT password FROM admins WHERE username=\"{}\"".format(username))
                stored_password = self.cur.fetchone()[0]
                is_valid = check_password_hash(stored_password, password)
                return is_valid

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

    def is_admin(self, username):
        """
        - Checks if a user is an admin.
        """
        done = self.cur.execute("SELECT username FROM admins WHERE username=\"{}\"".format(username))
        if done == 0:
            return False
        else:
            return True

    def add_user(self, username, password):
        """
        - Add the new user credentials to the USERS table.
        """
        password_hash = generate_password_hash(password)
        try:
            self.cur.execute("INSERT INTO users VALUES(\"{}\", \"{}\")".format(username, password_hash))
            self.db.commit()
        except:
            self.db.rollback()

    def delete_user(self, username):
        """
        - Deletes user credentials from the USERS table.
        """
        try:
            self.cur.execute("DELETE FROM users WHERE username = \"{}\"".format(username))
            self.db.commit()
        except:
            self.db.rollback()
