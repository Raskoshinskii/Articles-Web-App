from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response
import sqlite3
import os
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from UserLogin import UserLogin
from Forms import LoginForm, RegisterForm
# Import an instance of Blueprint class
from admin_panel.admin_panel import admin_panel

# App Configuration (Config variables must be CAPITALIZED)
DATABASE = 'tmp/site.db'
DEBUG = True
# Flash messages are defined in a session and a session must have a secret key
# This key must be set into app configuration
SECRET_KEY = 'as!!&sda3123y@##acsa5gf32sc'
# Set max size for files in bytes (1Mb)
MAX_CONTENT_LENGTH = 1024*1024

# Create the app and its configuration
app = Flask(__name__)
app.config.from_object(__name__)  # app configuration is a dictionary!
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'site.db')))  # a database will be created in the root_path
# Every Blueprint instance must be registered in the app.
app.register_blueprint(admin_panel, url_prefix='/admin_panel')

# To provide pages only for authorized users use LoginManager (it's much better than using cookies or sessions)
# To do that, link  an instance of LoginManager with the current app
login_manager = LoginManager(app)

# The function login will be called if a page is being accessing by an unauthorized users
login_manager.login_view = 'login'

# Writing our own messages for unauthorized users
login_manager.login_message = ' Please Log In For Accessing the Page'
login_manager.login_message_category = 'success'


@login_manager.user_loader
def load_user(user_id):
    """
    The function takes in an id from user session with the help of @login_manager.user_loader.
    Knowing the id we can then easily obtain a user from the DB and create an instance from UserLogin Class for the current user.
    This enables the module Flask-login to understand with what user it currently works with and provide an access to pages if
    the current user is logged-in
    """
    return UserLogin().from_db(user_id, dbase)


def connect_db():
    """Defines a connection with a database"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  # to return records as a dictionary
    return conn


def create_db():
    """Defines a function for a database creation"""
    db = connect_db()  # creates a database in the root_path
    # Add tables in the current database
    with app.open_resource('tables_creation.sql', mode='r') as sql_file:
        db.cursor().executescript(sql_file.read())  # if get errors, check the scripts in sql_file
    db.commit()
    db.close()


def get_db():
    """Setups a connection with DB"""
    # Check if object g has a property site.db. If not, create a connection with a database
    if not hasattr(g, 'site.db'):
        g.site_db = connect_db()
    return g.site_db

# To detect the beginning and the end of a request, use special decorators
# This decorator prevents repeating DB creation and closing in each route
dbase = None
@app.before_request
def before_request():
    """Creates a connection with a DB before request"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    """Closes the current connection with DB"""
    # If there is a connection with a DB, close it
    if hasattr(g, 'site.db'):
        g.link_db.close()


"""
DB FUNCTIONS MUST BE EXECUTED VIA CONSOLE! 
WHEN A REQUEST HAS COME (CONNECTION WITH DB IS TURN ON AND TURN OFF AFTER COMPLETING)
"""


@app.route('/')
def home():
    """Defines Home Page Functionality"""
    # Can pass parameters into render_template. These parameters are set into HTML templates
    # site_menu data will be obtained from DB
    return render_template('home.html', site_menu=dbase.get_menu(), articles=dbase.get_all_articles())


@app.route('/about')
def about():
    """Defines About page Functionality"""
    return render_template('about.html', title='About This Site', site_menu=dbase.get_menu())


@app.route('/contacts', methods=['POST', 'GET'])
def contacts():
    """Define Contacts Page Functionality"""
    # Only for requests with method POST
    if request.method == 'POST':
        # Accessing data from the submitted form
        print(request.form)
        # Accessing certain data from the from
        print('Message:', request.form['message'])

        # flash messages (instant messages that are depicted on a form when the form has been submitted)
        # For simplicity don't make a complex checking procedure for the username field
        if len(request.form['username']) > 2:
            # category is used for CSS
            flash('Your Message Has Been Sent', category='success')
        else:
            flash('An Error Has Occurred!\nTry Again', category='error')

    return render_template('contacts.html', title='Contacts', site_menu=dbase.get_menu())


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    """Define Profile Page Functionality"""
    return render_template('profile.html', title='Profile', site_menu=dbase.get_menu(), user_info=current_user.get_id())


@app.route('/user_avatar')
def user_avatar():
    """Defines user_avatar page functionality"""
    image = current_user.get_user_avatar(app)
    if not image:
        return ''

    header = make_response(image)
    header.headers['Content-Type'] = 'image/jpg'
    return header


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    """Defines a functionality for uploading"""
    if request.method == 'POST':
        file = request.files['file']
        # The method verify_extension verifies the extension of the file
        if file and current_user.verify_extension(file.filename):
            try:
                image = file.read()
                res = dbase.update_avatar(image, current_user.get_id())
                if not res:
                    flash("An Error Occurred While Updating Users's Avatar!", category='error')
                flash("User's Avatar Updated", category='success')
            except FileNotFoundError as error:
                flash('An Error Occurred While Reading the File', category='error')
        else:
            flash("An Error Occurred While Updating Users's Avatar!", category='error')

    return redirect(url_for('profile'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    """Defines Login Page Functionality"""
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    login_form = LoginForm()

    # The method validate_on_submit checks if the data was sent by POST method.
    # Besides, it validates the data by using validators in Forms class
    if login_form.validate_on_submit():
        user = dbase.get_user_by_username(login_form.username.data)
        if user and check_password_hash(user['password'], login_form.password.data):
            # After logging-in we have to create an instance of UserLogin class to store user's info
            user_login = UserLogin().create(user)
            is_remember = login_form.remember_me_button.data
            login_user(user_login, remember=is_remember)
            # To start from a page we wanted to access instead of profile page use the parameter next
            # If param next exists we will access next page otherwise the profile page will be accessed
            return redirect(request.args.get('next') or url_for('profile'))

        flash('The User Name/Password Is Incorrect', category='error')

    return render_template('login.html', title='Login', site_menu=dbase.get_menu(), form=login_form)


@app.route('/logout')
@login_required
def logout():
    """Defines Logout page functionality"""
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    """Defines Registration of a new user"""
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        hash = generate_password_hash(register_form.password_1.data)
        res = dbase.add_user(register_form.username.data, register_form.email.data, hash)
        if res:
            flash('You Have Been Successfully Signed-Up', category='success')
            return redirect(url_for('profile'))
        else:
            flash('An Error Has Occurred While Adding in DB!', category='error')

    return render_template('registration.html', title='SignUp', site_menu=dbase.get_menu(), form=register_form)


@app.route('/add_article', methods=['POST', 'GET'])
@login_required
def add_article():
    """Defines articles uploading new articles functionality"""
    if request.method == 'POST':
        if len(request.form['article_name']) > 4 and len(request.form['article_content']) > 10:
            res = dbase.add_article(request.form['article_name'], request.form['article_content'], request.form['article_url'])
            if not res:
                flash('An Error Has Occurred While Adding!', category='error')
            else:
                flash('The Article Has Been Successfully Added', category='success')
        else:
            flash('An Error Has Occurred While Adding!', category='error')

    return render_template('add_article.html', site_menu=dbase.get_menu(), title='New Article')


@app.route('/show_article/<alias>')
@login_required
def show_article(alias):
    """Defines functionality of depicting articles on the page"""
    article_name, article_content = dbase.get_article(alias)

    if not article_name:
        abort(404)

    return render_template('article.html', site_menu=dbase.get_menu(), title=article_name, content=article_content)


@app.errorhandler(404)
def page_not_found(error):
    """
    To catch and process errors use @app.errorhandler (error_num)
    Define a func for handling 404 error (page not found)
    """
    return render_template('page404.html', title='Page Not Found', site_menu=dbase.get_menu())




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

"""
IP address 0.0.0.0 isn't routable and isn't attached to a specific IP address."
Basically, it means all addresses IPv4 on localhost
In our case, the app will be available here: http://127.0.0.1:5000/

"""