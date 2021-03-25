from flask import Flask, render_template, redirect, request
from flask import send_file, session, Response
import random
import uuid
import json
from movies import get_movies
from usersdb import authorization, registration
import base64
from datetime import datetime
import time

app = Flask(__name__)

# Rooms tokens
tokens = {
}

# Users in system
users = {
}

# Movies rated in rooms
picks = {
}

# All movies
movies = []


@app.route("/favicon.ico")
def icon():
    return Response(status=404)


@app.route("/")
def home():
    if 'login' in session:
        return render_template("join.html", login=session['login'])
    else:
        return render_template("login.html")


@app.route("/logout", methods=['POST'])
def logout_fun():
    if 'login' in session:
        session.pop('login', None)
    return {
        "status": 1
    }


@app.route("/login")
def login_page():
    if 'login' in session:
        return render_template("join.html", login=session['login'])
    else:
        return render_template("login.html")


@app.route("/login", methods=['POST'])
def login_fun():
    login = request.form['login']
    password = request.form['password']

    if authorization(login, password):
        session['login'] = login
        return {
            "status": 1
        }
    else:
        return {
            "status": 0
        }


@app.route("/reg")
def reg_page():
    if 'login' in session:
        return render_template("join.html", login=session['login'])
    else:
        return render_template("reg.html")


@app.route("/reg", methods=['POST'])
def reg_fun():
    login = request.form['login']
    password = request.form['password']
    if len(password) < 6:
        return {
            "status": -1
        }

    if registration(login, password):
        session['login'] = login
        return {
            "status": 1
        }
    else:
        return {
            "status": 0
        }


@app.route("/create")
def new():
    if 'login' in session:
        token = generate_token()
        return render_template("create.html", login=session['login'], token=token)
    else:
        return render_template("login.html")


@app.route("/images/<image>")
def send_image(image):
    path = "images/" + image
    return send_file(path, mimetype='image/gif')


@app.route("/create", methods=['POST'])
def create():
    token = request.form['token']
    refresh_tokens()
    if token in tokens:
        return {
            "status": 0
        }
    else:
        tokens[token] = datetime.now()

        gid = token
        session['gid'] = gid
        uid = session['login']  # str(uuid.uuid1())
        users[uid] = set()
        picks[gid] = {}

        return {
            "status": 1
        }


@app.route("/join", methods=['POST'])
def join():
    token = request.form['token']
    refresh_tokens()
    if token in tokens:
        gid = token
        session['gid'] = gid
        uid = session['login']  # str(uuid.uuid1())
        users[uid] = set()
        if gid not in picks:
            picks[gid] = {}
        else:
            for movie in picks[gid]:
                picks[gid][movie][uid] = -1
        return {
            "status": 1
        }
    else:
        return {
            "status": 0
        }


@app.route("/pick")
def pick():
    gid = session['gid']
    uid = session['login']

    if gid not in picks or uid not in users:
        return redirect("/", code=302)
    match = check(gid, uid)
    if match:
        movie = movies[match]
        return render_template("match.html", fid=match, img=movie['img'], title=movie['title'], prod=movie['prod'],
                               year=movie['year'], rating=movie['rating'], summary=movie['summary'])

    if len(picks[gid].keys() - users[uid]) > 0:
        new_movies = picks[gid].keys() - users[uid]
        new_movie = random.sample(new_movies, 1)[0]
    else:
        if len(movies.keys() - users[uid]) > 0:
            new_movies = movies.keys() - users[uid]
            new_movie = random.sample(new_movies, 1)[0]
        else:
            return render_template("end.html")
    movie = movies[new_movie]

    return render_template("index.html", fid=new_movie, img=movie['img'], title=movie['title'], prod=movie['prod'],
                           year=movie['year'], rating=movie['rating'], summary=movie['summary'])


@app.route("/rerate/<fid>")
def rerate(fid):
    if fid in movies.keys():
        movie = movies[fid]
        return render_template("index.html", fid=fid, img=movie['img'], title=movie['title'], prod=movie['prod'],
                           year=movie['year'], rating=movie['rating'], summary=movie['summary'])


@app.route("/rated")
def rated_page():
    gid = session['gid']
    gmovies = {}
    for movie in picks[gid]:
        gmovies[movie] = movies[movie].copy()
        points = 0
        for user in picks[gid][movie]:
            if picks[gid][movie][user] >= 1:
                points += 1
        gmovies[movie]['grades'] = len(picks[gid][movie])
        gmovies[movie]['points'] = points

    def custom_sort(e):
        return e[1]['points']

    gmovies = {k: v for k, v in sorted(gmovies.items(), key=custom_sort, reverse=True)}

    return render_template("rated.html", movies=gmovies)


@app.route("/rate", methods=['POST'])
def rate():

    point = request.form['point']
    fid = request.form['fid']
    uid = session['login']  # request.form['uid']
    gid = session['gid']  # request.form['gid']
    if gid not in picks or uid not in users:
        return redirect("/", code=302)

    users[uid].add(fid)

    if fid not in picks[gid]:
        picks[gid][fid] = {}
    picks[gid][fid][uid] = int(point)

    return {
        "status": 1
    }


def check(gid, myuid):

    for fid in picks[gid]:
        found = False
        if len(picks[gid][fid]) > 1:
        	if not ((myuid in picks[gid][fid]) and (picks[gid][fid][myuid] == 2)):
		        for uid in picks[gid][fid]:
		            if picks[gid][fid][uid] < 1:
		                found = True
		        if not found:
		            return fid
    return False


def generate_token():
    while True:
        chars = random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6)

        token = ""
        for c in chars:
            token += c
        if token not in tokens:
            return token


def refresh_tokens():
    now = datetime.now()
    for token in list(tokens):
        if (now - tokens[token]).seconds > 86400:
            tokens.pop(token)


@app.route('/skip', methods=['POST'])
def skip():

    fid = request.form['fid']
    uid = session['login']  # request.form['uid']
    gid = session['gid']  # request.form['gid']

    picks[gid][fid][uid] = 2
    
    return {
        "status": 1
    }


@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def catch_all(u_path):
    return redirect("/", code=302)


if __name__ == "__main__":
    movies = get_movies()
    app.secret_key = 'asdfyth54gd3445765gdfvdfv'
    app.run(host="0.0.0.0", debug=False)
    
    

