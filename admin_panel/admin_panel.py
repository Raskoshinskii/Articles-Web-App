from flask import Blueprint, request, redirect, render_template, flash, url_for, session, g
import sqlite3
admin_panel = Blueprint('admin_panel', __name__, template_folder='templates', static_folder='static')
"""
Blueprint allows splitting a complex app into a set of individual modules
The less relationship between the modules and the app, the better 

admin_panel - Blueprint name it will be used as suffix for all methods of this module;
__name__ - name of the module where a directory admin_panel and other directories will be searched;
template_folder - a subdirectory for templates. If not provided, a folder of the app is taken;
static_folder - a subdirectory for static files. If not provided, a folder of the app is taken;
"""

"""
flask_login can be defined only in one app
we can't use flask_login for admin_login in admin_panel module
"""


def login_admin():
    session['is_admin_logged_in'] = 1


def is_admin_logged_in():
    return True if session.get('is_admin_logged_in') else False


def logout_admin():
    session.pop('is_admin_logged_in', None)


admin_panel_menu = [{'url': '.index', 'title': 'Panel'},
                    {'url': '.logout', 'title': 'Logout'},
                    {'url': '.list_articles', 'title': 'List of Articles'},
                    {'url': '.list_users', 'title': 'Registered Users'},
                    {'url': 'home', 'title': 'Main Site'}]

"""Define a connection with the DB"""
db = None
@admin_panel.before_request
def before_request():
    global db
    db = g.get('site_db')

@admin_panel.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@admin_panel.route('/')
def index():
    if not is_admin_logged_in():
        return redirect('.login')

    return render_template('admin_panel/index.html', menu=admin_panel_menu, title='Admin Panel')


@admin_panel.route('/login', methods=['POST', 'GET'])
def login():

    if is_admin_logged_in():
        return redirect(url_for('.index'))

    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            login_admin()
            # The dot means that the function index must be taken from the current blueprint, not global from the app!
            return redirect(url_for('.index'))
        else:
            flash('Username or Password Is Incorrect', category='error')

    return render_template('admin_panel/login.html', title='Admin Panel')


@admin_panel.route('/logout', methods=['POST', 'GET'])
def logout():
    if not is_admin_logged_in():
        redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))


@admin_panel.route('/list_articles')
def list_articles():
    if not is_admin_logged_in():
        return redirect((url_for('.login')))

    list_articles = []

    if db:
        try:
            print('a')
            cur = db.cursor()
            cur.execute('SELECT title, content, url FROM articles')
            list_articles = cur.fetchall()
        except sqlite3.Error as error:
            print('An Error occurred While Extracting the Data from the DB\n', error)

    return render_template('admin_panel/list_articles.html', title='List of Articles', menu=admin_panel_menu, list=list_articles)


@admin_panel.route('/list_users')
def list_users():
    if not is_admin_logged_in():
        return redirect((url_for('.login')))

    user_lst = []

    try:
        cur = db.cursor()
        cur.execute('SELECT name, email FROM users ORDER BY time DESC')
        user_lst = cur.fetchall()
    except sqlite3.Error as error:
        print('An Error Occurred While Extracting the Data from the DB\n', error)

    return render_template('admin_panel/user_list.html', title='List of Users', menu=admin_panel_menu, list=user_lst)