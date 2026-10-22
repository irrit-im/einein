from flask import *

STATIC_DIR = "static"
IMAGE_DIR = "static/img"
ACCOUNTS = {
    "NotCookieMonster": "I<3Cookies",
    "Grover": None, # Password redacted! You don't know this password :(
    "Elmo": None, # Password redacted! You don't know this password :(
    "CountVonCount": None, # Password redacted! You don't know this password :(
    "OscarTheGrouch": None, # Password redacted! You don't know this password :(
    "BigBird": None, # Password redacted! You don't know this password :(
    "CookieMonster": "I<3Cookies",
    "Bert": None, # Password redacted! You don't know this password :(
    "Ernie": None, # Password redacted! You don't know this password :(
}
ACCOUNT_LIST = list(ACCOUNTS.keys())[::-1]
BANNED = {"OscarTheGrouch", "CookieMonster", "NotCookieMonster"}

app = Flask(__name__)

def render_page(page, **kwargs):
    username = request.cookies.get('username')
    if username is not None:
        kwargs['name'] = username
    return render_template(page, **kwargs)


@app.route('/img/<image>')
def images(image):
    return send_from_directory(IMAGE_DIR, image)


@app.route('/static/<path>')
def static_files(path):
    return send_from_directory(STATIC_DIR, path)


@app.route('/')
def home():
    return render_page("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_page("login.html")

    username = request.form.get('username', default='')
    password = request.form.get('password', default='')

    if username not in ACCOUNTS or ACCOUNTS[username] != password:
        return render_page("login.html", error="Invalid Login")
    
    resp = make_response(redirect('/'))
    resp.set_cookie('username', username)
    resp.set_cookie('uid', f"{ACCOUNT_LIST.index(username)}")

    return resp

@app.route('/community')
def community():
    users = [(user, True) if user in BANNED else (user, False)
             for user in ACCOUNT_LIST]
    return render_page("community.html", users=users)

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('username')
    resp.delete_cookie('uid')

    return resp

@app.route('/vault')
def vault():
    username = request.cookies.get('username')
    uid = request.cookies.get('uid')
    if username is None or uid is None:
        return abort(403, description="You must be logged in to access the vault.")
    if username not in ACCOUNTS or f"{ACCOUNT_LIST.index(username)}" != uid:
        return abort(403, description="Invalid user login, try to log in again.")
    if username in BANNED:
        return abort(403, description="You are banned from the vault.")
    return render_page("vault.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80")
