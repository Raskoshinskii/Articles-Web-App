from flask_login import UserMixin
from flask import url_for


class UserLogin(UserMixin):
    """
    This class was created to be ables using LoginManager.
    The class describes the info about the current user
    The following methods must be defined:
    - is_authenticated
    - is_active
    - is_anonymous
    - get_id

    All above methods will be used by the function login_user() to insert into a session the current user's info

    !!! class UserMixin can be used then we don't need to provide the following methods:
    - is_authenticated
    - is_active
    - is_anonymous
    """
    def create(self, user):
        self.__user = user
        return self

    def from_db(self, user_id, db):
        self.__user = db.get_user(user_id)
        return self

    def get_id(self):
        return str(self.__user['id'])

    def get_name(self):
        return self.__user['name'] if self.__user else 'No Name'

    def get_email(self):
        return self.__user['email'] if self.__user else 'No Email'

    def get_user_avatar(self, app):
        image = None
        # If there is no avatar, download a default one
        if not self.__user['user_avatar']:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='images_html/default.jpg'), 'rb') as file:
                    image = file.read()
            except FileNotFoundError as error:
                print('Default Avatar Not Found!\nError: ', error)
        else:
            image = self.__user['user_avatar']

        return image

    def verify_extension(self, filename):
        extension = filename.rsplit('.', 1)[1]
        if extension.lower() in ['jpg','png']:
            return True
        else:
            return False


