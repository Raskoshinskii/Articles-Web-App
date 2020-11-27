import math, sqlite3, time


class FDataBase:
    """Class for accessing/uploading the data from/into the DB"""
    # In constructor define the cursor
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    # getMenu function returns data for site menu from the DB
    def get_menu(self):
        query = """SELECT * FROM site_menu"""
        try:
            self.__cur.execute(query)
            res = self.__cur.fetchall()
            if res:
                return res
        # If an exception occurs, print the error message and retunr an empty list
        except:
            print('DataBase Reading Error')

        return []

    def add_article(self, title, content, article_url):
        # Try adding a new record into the DB
        try:
            # Check whether an article exists or not
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM articles WHERE url LIKE '{article_url}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('The Article With This URL Already Exists!')
                return False

            # If not exists, add it
            # Get time of article creation
            time_creation = math.floor(time.time())
            # Add the data into the DB

            self.__cur.execute('INSERT INTO articles VALUES (NULL, ?, ?, ?, ?)', (title, content, article_url, time_creation))
            # Always commit the changes into the current DB
            self.__db.commit()

        # Show the error message if can't write into the DB
        except sqlite3.Error as error:
            print('An Error Has Occurred While Inserting Data Into the Database\nType Error:', error)
            return False

        return True

    def get_article(self, alias):
        try:
            self.__cur.execute(f"SELECT title, content FROM articles WHERE url LIKE '{alias}' ")
            res = self.__cur.fetchone()
            if res:
                return res

        except sqlite3.Error as error:
            print('An Error Has Occurred While Extracting the Data From the Database\nType Error:', error)

        return (False, False)

    def get_all_articles(self):
        try:
            self.__cur.execute(f'SELECT id, title, content, url FROM articles ORDER BY creation_date DESC')
            res = self.__cur.fetchall()
            if res:
                return res

        except sqlite3.Error as error:
            print('An Error Has Occurred While Obtaining the Articles From the Database\nType Error:', error)

        return []

    def add_user(self, name, email, hashed_psw):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('A User With This Email Already Exists!')
                return False

            time_creation = math.floor(time.time())
            self.__cur.execute('INSERT INTO users VALUES (NULL, ?, ?, ?, NULL, ?)', (name, email, hashed_psw, time_creation))
            self.__db.commit()

        except sqlite3.Error as error:
            print('An Error Has Occurred While Inserting a New User Into the Database\nType Error:', error)
            return False

        return True

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print('The User Not Found!')
                return False

            return res

        except sqlite3.Error as error:
            print('An Error Has Occurred While Extracting the Data From the Database\nType Error:', error)

        return False

    def get_user_by_username(self, username):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE name = '{username}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print('The user Is Not Found!')
                return False

            return res

        except sqlite3.Error as error:
            print('An Error Has Occurred While Extracting the Data From the Database\nType Error:', error)

        return False

    def update_avatar(self, user_avatar, user_id):
        if not user_avatar:
            return False

        try:
            # Create a special binary object for inserting in DB
            binary = sqlite3.Binary(user_avatar)
            self.__cur.execute('UPDATE users SET user_avatar = ? WHERE id = ?', (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as error:
            print('An Error Has Occurred While Updating the Avatar\nType Error:', error)
            return False

        return True
