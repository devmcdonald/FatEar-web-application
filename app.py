from flask import Flask, render_template, request, session, url_for, redirect, flash
import bcrypt
import datetime
from datetime import date
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import binascii

# Start app
app = Flask(__name__)

# Set environment variables - local development
"""
load_dotenv("secrets.env")
SECRET_KEY = os.getenv("SECRET_KEY")
app.secret_key = SECRET_KEY
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

"""
# Set environment variables - production
SECRET_KEY = os.environ.get("SECRET_KEY")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])



app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

# Configure PostgreSQL database- TO DO
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    dbname=DB_NAME
)
db = SQLAlchemy()
# Set DB_PASSWORD in env variable before deployment
db.init_app(app)


# Define a route to hello function
@app.route("/")
def hello():
    return render_template("index.html")


# Define route for song searching
@app.route("/songSearch", methods=["GET", "POST"])
def songSearch():
    artist = request.form["artist"]
    genre = request.form["genre"]
    rating = request.form["rating"]

    # cursor used to send queries
    cursor = conn.cursor()
    error = None
    # determine which query to execute
    if artist and not genre and not rating:
        query = """
            SELECT song.title AS title, 
                (artist.fname || ' ' || artist.lname) AS artistName, 
                album.title AS albumTitle, 
                ROUND(AVG(stars), 2) AS avgrating, 
                songID, 
                genre 
            FROM ((((song 
            NATURAL JOIN artistperformssong) 
            NATURAL JOIN artist) 
            NATURAL JOIN songgenre) 
            NATURAL JOIN songinalbum) 
            JOIN album USING(albumID) 
            JOIN ratesong USING(songID) 
            GROUP BY songID, artist.fname, artist.lname, song.title, album.title, genre 
            HAVING (artist.fname || ' ' || artist.lname) ILIKE %s
        """
        cursor.execute(query, ("%" + artist + "%",))

    elif not artist and genre and not rating:
        query = """
            SELECT song.title AS title, 
                (artist.fname || ' ' || artist.lname) AS artistName, 
                album.title AS albumTitle,
                ROUND(AVG(stars), 2) AS avgrating, 
                songID, 
                genre 
            FROM ((((song 
            NATURAL JOIN artistperformssong) 
            NATURAL JOIN artist) 
            NATURAL JOIN songgenre) 
            NATURAL JOIN songinalbum) 
            JOIN album USING(albumID) 
            JOIN ratesong USING(songID) 
            GROUP BY songID, artist.fname, artist.lname, song.title, album.title, genre 
            HAVING genre ILIKE %s
            """
        cursor.execute(query, ("%" + genre + "%",))

    elif not artist and not genre and rating:
        query = """
            SELECT song.title AS title, 
                (artist.fname || ' ' || artist.lname) AS artistName, 
                album.title AS albumTitle, 
                ROUND(AVG(stars), 2) AS avgrating, 
                songID, 
                genre 
            FROM ((((song 
            NATURAL JOIN artistperformssong) 
            NATURAL JOIN artist) 
            NATURAL JOIN songgenre) 
            NATURAL JOIN songinalbum) 
            JOIN album USING(albumID) 
            JOIN ratesong USING(songID) 
            GROUP BY songID, artist.fname, artist.lname, song.title, album.title, genre 
            HAVING ROUND(AVG(stars), 2) >= %s
            """
        cursor.execute(query, (rating))

    elif artist and genre and not rating:
        query = """
            SELECT song.title AS title, 
                (artist.fname || ' ' || artist.lname) AS artistName, 
                album.title AS albumTitle, 
                ROUND(AVG(stars), 2) AS avgrating, 
                songID, 
                genre 
            FROM ((((song 
            NATURAL JOIN artistperformssong) 
            NATURAL JOIN artist) 
            NATURAL JOIN songgenre) 
            NATURAL JOIN songinalbum) 
            JOIN album USING(albumID) 
            JOIN ratesong USING(songID) 
            GROUP BY songID, artist.fname, artist.lname, song.title, album.title, genre 
            HAVING (artist.fname || ' ' || artist.lname) ILIKE %s and genre ILIKE %s
        """
        
        cursor.execute(query, ("%" + artist + "%", "%" + genre + "%"))

    elif artist and not genre and rating:
        query = """
            SELECT song.title AS title, 
                (artist.fname || ' ' || artist.lname) AS artistName, 
                album.title AS albumTitle, 
                ROUND(AVG(stars), 2) AS avgrating, 
                songID, 
                genre 
            FROM ((((song 
            NATURAL JOIN artistperformssong) 
            NATURAL JOIN artist) 
            NATURAL JOIN songgenre) 
            NATURAL JOIN songinalbum) 
            JOIN album USING(albumID) 
            JOIN ratesong USING(songID) 
            GROUP BY songID, artist.fname, artist.lname, song.title, album.title, genre 
            HAVING (artist.fname || ' ' || artist.lname) ILIKE %s and ROUND(AVG(stars), 2) >= %s
        """
        
        cursor.execute(query, ("%" + artist + "%", rating))

    elif not artist and genre and rating:
        query = """
            SELECT song.title AS title, 
                (artist.fname || ' ' || artist.lname) AS artistName, 
                album.title AS albumTitle, 
                ROUND(AVG(stars), 2) AS avgrating, 
                songID, 
                genre 
            FROM ((((song 
            NATURAL JOIN artistperformssong) 
            NATURAL JOIN artist) 
            NATURAL JOIN songgenre) 
            NATURAL JOIN songinalbum) 
            JOIN album USING(albumID) 
            JOIN ratesong USING(songID) 
            GROUP BY songID, artist.fname, artist.lname, song.title, album.title, genre 
            HAVING genre ILIKE %s and ROUND(AVG(stars), 2) >= %s
        """
        
        cursor.execute(query, ("%" + genre + "%", rating))

    elif artist and genre and rating:
        query = """
            SELECT song.title AS title, 
                (artist.fname || ' ' || artist.lname) AS artistName, 
                album.title AS albumTitle, 
                ROUND(AVG(stars), 2) AS avgrating, 
                songID, 
                genre 
            FROM ((((song 
            NATURAL JOIN artistperformssong) 
            NATURAL JOIN artist) 
            NATURAL JOIN songgenre) 
            NATURAL JOIN songinalbum) 
            JOIN album USING(albumID) 
            JOIN ratesong USING(songID) 
            GROUP BY songID, artist.fname, artist.lname, song.title, album.title, genre 
            HAVING (artist.fname || ' ' || artist.lname) ILIKE %s and genre ILIKE %s and ROUND(AVG(stars), 2) >= %s
        """
        
        cursor.execute(query, ("%" + artist + "%", "%" + genre + "%", rating))

    else:
        if "username" in session:
            return home(error="Invalid Search")
        else:
            return render_template("index.html", error="Invalid Search")

    # stores the results in a variable
    data = cursor.fetchall()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    
    # Convert rows to dictionaries for easier template rendering
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in data]
    
    return render_template("songSearch.html", song_list=data, error=error)


# Define route for login
@app.route("/login")
def login():
    return render_template("login.html")


# Define route for register
@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/loginAuth", methods=["GET", "POST"])
def loginAuth():
    # grabs information from the forms
    username = request.form["username"]
    password = request.form["password"].encode('utf-8')

    # cursor used to send queries
    cursor = conn.cursor()
    
    # executes query
    query = "SELECT pwd FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    
    # stores the results in a variable
    result = cursor.fetchone()
    cursor.close()
    
    error = None
    if result:
        hashed_hex = result[0]  # fetchone() returns a tuple, so use index 0
        
        try:
            # Convert the hex string back to bytes
            stored_hash = binascii.unhexlify(hashed_hex)
            
            if bcrypt.checkpw(password, stored_hash):
                # creates a session for the user
                session["username"] = username
                return redirect(url_for("home"))
            else:
                error = "Invalid password"
        except ValueError as ve:
            print(f"ValueError: {ve}")  # Debug print
            error = "An error occurred. Please try again."
    else:
        error = "Invalid username"
    
    return render_template("login.html", error=error)


@app.route("/registerAuth", methods=["GET", "POST"])
def registerAuth():
    # grabs information from the forms
    username = request.form["username"]
    password = request.form["password"].encode('utf-8')
    fname = request.form["fname"]
    lname = request.form["lname"]
    nickname = request.form["nickname"]

    # Salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    hashed_hex = binascii.hexlify(hashed).decode('utf-8')  # Convert to hex string for storage
    
    # cursor used to send queries
    cursor = conn.cursor()
    
    # executes query
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))  # Note the comma to make it a single-item tuple
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if data:
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template("register.html", error=error)
    else:
        ins = "INSERT INTO users (username, pwd, fname, lname, lastlogin, nickname) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(ins, (username, hashed_hex, fname, lname, date.today(), nickname))
        conn.commit()
        cursor.close()
        return render_template("index.html")


@app.route("/home")
def home(error=None):
    if "username" not in session:
        return render_template("index.html", error="User Not Logged In")
    else:
        user = session["username"]
        cursor = conn.cursor()
        # Query 2 finds reviews of friends since my last login
        query2 = "\
            (select username, album.title AS albumName, '' as songID, title, reviewText, reviewDate \
            from reviewAlbum join album using(albumID)\
            where username = %s AND reviewDate > \
                (select lastlogin \
                from users \
                where username = %s) \
            AND \
                username in (\
                    select F.user2 as username\
                    from friend as F\
                    where F.user1 = %s and F.acceptStatus = 'Accepted' \
                UNION distinct\
                    select S.user1 as username\
                    from friend as S\
                    where S.user2 = %s and S.acceptStatus = 'Accepted') \
                    OR username in\
                    (select follows as username\
                    from follows\
                    where follower = %s))\
            UNION\
            (select username, null as albumName, songID, title, reviewText, reviewDate\
            from reviewSong join song using(songID)\
            where username = %s AND reviewDate >\
                (select lastlogin\
                from users\
                where username = %s) \
            AND\
                username in (\
                    select F.user2 as username \
                    from friend as F\
                    where F.user1 = %s and F.acceptStatus = 'Accepted' \
                UNION distinct\
                    select S.user1 as username\
                    from friend as S\
                    where S.user2 = %s and S.acceptStatus = 'Accepted') \
                    OR username in\
                    (select follows as FollowedUsers\
                    from follows\
                    where follower = %s));"

        
        cursor.execute(query2, (user, user, user, user, user, user, user, user, user, user))
        data2 = cursor.fetchall()
        # Convert reviews into a list of dictionaries
        review_columns = [desc[0] for desc in cursor.description]
        reviews = [dict(zip(review_columns, row)) for row in data2]
        
        query3 = "SELECT (artist.fname || ' ' || artist.lname) AS artistName, songID, title\
            FROM ((((users NATURAL JOIN userfanofartist) NATURAL JOIN artistperformssong) NATURAL JOIN song ) JOIN artist using(artistID))\
            WHERE username = %s and releaseDate > lastlogin"
        cursor.execute(query3, (user,))
        data3 = cursor.fetchall()
        
        # Convert new songs into a list of dictionaries
        song_columns = [desc[0] for desc in cursor.description]
        newsongs = [dict(zip(song_columns, row)) for row in data3]
        
        query4 = "SELECT fname, lname FROM users WHERE username = %s"
        cursor.execute(query4, (user,))
        data4 = cursor.fetchone()
        
        # Convert the result into a dictionary
        realname = {'fname': data4[0], 'lname': data4[1]} if data4 else {'fname': '', 'lname': ''}
        
        cursor.close()
        
        return render_template(
            "home.html",
            username=user,
            reviews=reviews,
            newsongs=newsongs,
            realname=realname,
            error=error,
        )


@app.route("/select_song/<songID>", methods=["GET", "POST"])
def select_song(songID, error=None):
    # username = session["username"]
    cursor = conn.cursor()
    query1 = "SELECT songID, song.title as title, (artist.fname || ' ' || artist.lname) AS artistName, genre, releaseDate, songURL, album.title as albumTitle, ROUND(AVG(stars), 2) AS avgrating, artistID \
        FROM (((((song natural join songgenre) natural join artistperformssong) join artist using(artistID)) natural join songinalbum) join album using(albumID) )join ratesong using(songID)\
        GROUP BY songID, song.title, artistName, genre, releaseDate, songURL, albumTitle, artistID \
        HAVING songID = %s "

    cursor.execute(query1, (songID,))
    songdata = cursor.fetchall()
    # Convert song data into a list of dictionaries
    song_columns = [desc[0] for desc in cursor.description]
    songs = [dict(zip(song_columns, row)) for row in songdata]
    
    query2 = "SELECT * FROM reviewsong WHERE songID = %s"
    cursor.execute(query2, (songID,))
    reviews = cursor.fetchall()
    
    # Convert new songs into a list of dictionaries
    review_columns = [desc[0] for desc in cursor.description]
    review_data = [dict(zip(review_columns, row)) for row in reviews]
    cursor.close()
    return render_template(
        "select_song.html", song_info=songs, reviews=review_data, error=error
    )


@app.route("/post", methods=["POST"])
def post():
    
    if "username" not in session:
        songID = request.form["songID"]
        return select_song(songID, error="Cannot Review - User Not Logged In")
    else:
        error = None
        username = session["username"]
        cursor = conn.cursor()
        review = request.form["reviewText"]
        songID = request.form["songID"]
        
        query0 = (
            "SELECT username, songID FROM reviewsong where username=%s and songID=%s"
        )
        cursor.execute(query0, (username, songID))
        safetynet = cursor.fetchall()
        if safetynet:  # review already exists
            error = "User already reviewed this song."
            return select_song(songID, error)

        query = "INSERT INTO reviewsong (username, songID, reviewText, reviewDate) VALUES(%s, %s, %s, %s)"
        cursor.execute(query, (username, songID, review, date.today()))
        conn.commit()
        cursor.close()
        return redirect(url_for("select_song", songID=songID))


@app.route("/rate_song", methods=["GET"])
def rate_song():
    if "username" not in session:
        songID = request.args["songID"]
        return select_song(songID, error="Cannot Rate - User Not Logged In")
    else:
        username = session["username"]
        cursor = conn.cursor()
        songID = request.args["songID"]
        stars = request.args["numStars"]

        query0 = "SELECT username, songID FROM ratesong WHERE username=%s and songID=%s"
        cursor.execute(query0, (username, songID))
        safetynet = cursor.fetchall()
        error = None
        if safetynet:  # rating already exists
            error = "User already rated this song."
            return select_song(songID, error)

        query = "INSERT INTO ratesong (username, songID, stars, ratingDate) VALUES(%s, %s, %s, %s)"
        cursor.execute(query, (username, songID, stars, date.today()))
        conn.commit()
        cursor.close()
        return redirect(url_for("select_song", songID=songID))


@app.route("/curr_friends")
def curr_friends():
    if "username" not in session:
        return render_template("index.html", error="User Not Logged In")
    else:
        username = session["username"]
        cursor = conn.cursor()
        query = "select F.user2 as username, users.fname as fname, users.lname as lname \
            from friend as F join users on (F.user2=users.username)\
            where F.user1 = %s and F.acceptStatus = 'Accepted'  \
            UNION distinct \
            select S.user1 as username, users.fname, users.lname \
            from friend as S join users on (S.user1=users.username)\
            where S.user2 = %s and S.acceptStatus = 'Accepted'"

        cursor.execute(query, (username, username,))
        data = cursor.fetchall()
        # Convert into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        friends = [dict(zip(columns, row)) for row in data]
        
        cursor.close()
        return render_template("curr_friends.html", username=username, friendlist=friends)


@app.route("/pending_requests")
def pending_requests():
    if "username" not in session:
        return render_template("index.html", error="User Not Logged In")
    else:
        username = session["username"]
        cursor = conn.cursor()
        query = "select user1 as requester \
            from friend \
            where user2 = %s and acceptStatus = 'Pending' and requestSentBy = user1 \
            UNION \
            select user2 as requester \
            from friend \
            where user1 = %s and acceptStatus = 'Pending' and requestSentBy = user2"

        cursor.execute(query, (username, username,))
        data = cursor.fetchall()
        # Convert into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        friends = [dict(zip(columns, row)) for row in data]
        cursor.close()
        return render_template("pending_requests.html", username=username, requests=friends)


@app.route("/accept_req/<user>")
def accept_req(user):
    if "username" not in session:
        return render_template("index.html", error="User Not Logged In")
    else:
        username = session["username"]
        cursor = conn.cursor()
        query = "UPDATE friend SET acceptStatus = 'Accepted' WHERE (user1 = %s AND user2 = %s) OR (user2 = %s AND user1 = %s)"
        cursor.execute(query, (username, user, username, user))
        conn.commit()
        cursor.close()
        return redirect(url_for("pending_requests"))


@app.route("/deny_req/<user>")
def deny_req(user):
    if "username" not in session:
        return render_template("index.html", error="User Not Logged In")
    else:
        username = session["username"]
        cursor = conn.cursor()
        query = "UPDATE friend SET acceptStatus = 'Not Accepted' WHERE (user1 = %s AND user2 = %s) OR (user2 = %s AND user1 = %s)"
        cursor.execute(query, (username, user, username, user))
        conn.commit()
        cursor.close()
        return redirect(url_for("pending_requests"))


@app.route("/search_users")
def search_users():
    if "username" not in session:
        return render_template("index.html", error="User Not Logged In")
    else:
        username = session["username"]
        friend = request.args["user"]
        cursor = conn.cursor()
        query = "SELECT username, (fname || ' ' || lname) as name FROM users WHERE (username like %s OR (fname || ' ' || lname) like %s) and username <> %s"
        cursor.execute(query, ("%" + friend + "%", "%" + friend + "%", username))
        data = cursor.fetchall()
        if data:
            # Convert into a list of dictionaries
            columns = [desc[0] for desc in cursor.description]
            people = [dict(zip(columns, row)) for row in data]
            return render_template("searched_users.html", result=people)
        else:
            error = "No users found"
            return home(error)


@app.route("/follow/<person>")
def follow(person):
    if "username" not in session:
        return render_template("index.html", error="User Not Logged In")
    else:
        username = session["username"]
        cursor = conn.cursor()

        query0 = "SELECT* FROM follows WHERE follower=%s and follows=%s"
        cursor.execute(query0, (username, person))
        safetynet = cursor.fetchall()
        error = None
        if safetynet:  # rating already exists
            error = "You already follows this user."
            return user(person, error)

        query = "INSERT INTO follows(follower, follows, createdAt) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, person, datetime.datetime.now()))
        conn.commit()
        cursor.close()
        return redirect(url_for("home"))


@app.route("/send_req/<person>")
def send_req(person):
    if "username" not in session:
        return render_template("index.html", error="User Not Logged In")
    else:
        username = session["username"]
        cursor = conn.cursor()

        query0 = (
            "SELECT* FROM friend WHERE (user1=%s and user2=%s) OR (user2=%s and user1=%s)"
        )
        cursor.execute(query0, (username, person, username, person))
        safetynet = cursor.fetchall()
        error = None
        if safetynet:  # request already exists
            error = "A friend request already exists for this user."
            return user(person, error)

        query = "INSERT INTO friend(user1, user2, acceptStatus, requestSentBy, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(
            query,
            (
                username,
                person,
                "Pending",
                username,
                datetime.datetime.now(),
                datetime.datetime.now(),
            ),
        )
        conn.commit()
        cursor.close()
        return redirect(url_for("home"))


@app.route("/followed_artists")
def followed_artists():
    if "username" not in session:
        return render_template("index.html", error="User Not Logged In")
    else:
        username = session["username"]
        cursor = conn.cursor()

        query = "select artistID, (artist.fname || ' ' || artist.lname) AS artistName, artistBio, artistURL\
            from userfanofartist NATURAL JOIN artist \
            where username = %s"

        cursor.execute(query, (username,))
        data = cursor.fetchall()
        # Convert into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        artists = [dict(zip(columns, row)) for row in data]
        
        cursor.close()
        return render_template("followed_artists.html", username=username, artistList=artists)


@app.route("/artist/<artistID>")
def artist(artistID, error=None):
    if "username" not in session:
        return render_template("index.html", error="User Not Logged In")
    else:
        
        cursor = conn.cursor()
        songQuery = "SELECT songID, song.title AS title, releaseDate, genre, ROUND(AVG(stars), 2) AS avgrating FROM artistperformssong NATURAL JOIN song NATURAL JOIN songgenre NATURAL JOIN ratesong GROUP BY songID, title, releaseDate, genre, artistID HAVING artistID = %s"
        cursor.execute(songQuery, (artistID,))
        songResults = cursor.fetchall()

        # Convert into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        songs = [dict(zip(columns, row)) for row in songResults]
        
        albumQuery = "SELECT albumID, album.title as title, ROUND(AVG(stars), 2) AS avgrating FROM artistperformssong NATURAL JOIN song NATURAL JOIN songinalbum JOIN album using(albumID) NATURAL JOIN ratealbum GROUP BY albumID, album.title, artistID HAVING artistID = %s"
        cursor.execute(albumQuery, (artistID,))
        albumResults = cursor.fetchall()
        # Convert into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        albums = [dict(zip(columns, row)) for row in albumResults]

        artistQuery = "SELECT (artist.fname || ' ' || artist.lname) AS artistName, artistBio, artistURL, artistID FROM artist WHERE artistID=%s"
        cursor.execute(artistQuery, (artistID,))
        artistResults = cursor.fetchall()
        # Convert into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        artists = [dict(zip(columns, row)) for row in artistResults]

        cursor.close()
        return render_template(
            "artist.html",
            songResults=songs,
            albumResults=albums,
            artistResults=artists,
            error=error,
        )


@app.route("/become_fan/<artistID>")
def become_fan(artistID):
    if "username" not in session:
        return artist(artistID, error="Cannot Become Fan - User Not Logged In")
    else:
        username = session["username"]
        cursor = conn.cursor()

        query0 = "SELECT * FROM userfanofartist WHERE username=%s and artistID=%s"
        cursor.execute(query0, (username, artistID))
        safetynet = cursor.fetchall()

        error = None
        if safetynet:  # already exists
            error = "User already fan of this user."
            return artist(artistID, error)
            # return redirect(url_for("artist/" + artistID))

        query = "INSERT INTO userfanofartist(username, artistID) VALUES (%s, %s)"
        cursor.execute(query, (username, artistID))
        conn.commit()
        cursor.close()
        return artist(artistID)
        # return redirect(url_for("artist"+ artistID))


@app.route("/search_artists")
def search_artists():
    if "username" not in session:
        return render_template("index.html", error="User Not Logged In")
    else:
        username = session["username"]
        search = request.args["search"]
        cursor = conn.cursor()
        query = "SELECT artistID, (artist.fname || ' ' || artist.lname) AS artistName FROM artist WHERE artistID like %s OR (artist.fname || ' ' || artist.lname) like %s"
        cursor.execute(query, ("%" + search + "%", "%" + search + "%"))
        data = cursor.fetchall()
        # Convert into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        artists = [dict(zip(columns, row)) for row in data]
        if data:
            return render_template("searched_artists.html", result=artists)
        else:
            error = "No artists found"
            return home(error)


@app.route("/user/<user>")
def user(user, error=None):
    if "username" not in session:
        return render_template("index.html", error="User Not Logged In")
    else:
        username = session["username"]  # must be logged in
        cursor = conn.cursor()
        userQuery = "SELECT username, concat(fname, ' ', lname) as name, lastlogin, nickname FROM users WHERE username = %s"
        cursor.execute(userQuery, (user,))
        userInfo = cursor.fetchall()
        # Convert into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        myInfo = [dict(zip(columns, row)) for row in userInfo]
        
        artistQuery = "SELECT artistID, concat(fname, ' ', lname) as artistName, artistBio, artistURL FROM userfanofartist NATURAL JOIN artist WHERE username = %s"
        cursor.execute(artistQuery, (user,))
        artistResults = cursor.fetchall()
        # Convert into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        artists = [dict(zip(columns, row)) for row in artistResults]

        songRatingQuery = "SELECT songID, stars, ratingDate, title, concat(artist.fname, ' ', artist.lname) AS artistName, artistID FROM ratesong NATURAL JOIN song NATURAL JOIN artistperformssong JOIN artist using(artistID) WHERE username = %s"
        cursor.execute(songRatingQuery, (user,))
        songRatings = cursor.fetchall()
        # Convert into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        songsRat = [dict(zip(columns, row)) for row in songRatings]

        songReviewQuery = "SELECT songID, reviewText, reviewDate, title, concat(artist.fname, ' ', artist.lname) AS artistName, artistID FROM reviewsong NATURAL JOIN song NATURAL JOIN artistperformssong JOIN artist using(artistID) WHERE username = %s"
        cursor.execute(songReviewQuery, (user,))
        songReviews = cursor.fetchall()
        # Convert into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        songsRev = [dict(zip(columns, row)) for row in songReviews]

        albumRatingQuery = "SELECT albumID, stars, title, concat(artist.fname, ' ', artist.lname) AS artistName, artistID FROM ratealbum NATURAL JOIN album NATURAL JOIN songinalbum NATURAL JOIN artistperformssong JOIN artist using(artistID) WHERE username = %s"
        cursor.execute(albumRatingQuery, (user,))
        albumRatings = cursor.fetchall()
        # Convert into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        albumRats = [dict(zip(columns, row)) for row in albumRatings]

        albumReviewQuery = "SELECT albumID, reviewText, reviewDate, album.title as albumTitle, concat(artist.fname, ' ', artist.lname) AS artistName, artistID FROM reviewalbum NATURAL JOIN album NATURAL JOIN songinalbum NATURAL JOIN artistperformssong JOIN artist using(artistID) WHERE username = %s"
        cursor.execute(albumReviewQuery, (user,))
        albumReviews = cursor.fetchall()
        # Convert into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        albumRevs = [dict(zip(columns, row)) for row in albumReviews]

        cursor.close()
        return render_template(
            "user.html",
            userInfo=myInfo,
            artistResults=artists,
            songRatings=songsRat,
            songReviews=songsRev,
            albumRatings=albumRats,
            albumReviews=albumRevs,
            error=error,
        )


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")


# Set debug to false in production envi
if __name__  == "__main__":
    app.run(debug=False)
    

