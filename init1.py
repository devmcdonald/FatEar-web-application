# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors, bcrypt
import datetime
from datetime import date


# for uploading photo:
from app import app

# from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


###Initialize the app from Flask
# app = Flask(__name__)
# app.secret_key = "secret key"

# Configure MySQL
conn = pymysql.connect(
    host="localhost",
    port=8889,
    user="root",
    password="root",
    db="fatear",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)


def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


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
        query = "SELECT song.title as title, concat(fname, ' ', lname) AS artistName, album.title as albumTitle, avg(stars) as avgrating, songID, genre \
            FROM ((((song NATURAL JOIN artistperformssong) NATURAL JOIN artist) NATURAL JOIN songgenre) NATURAL JOIN songinalbum) join album using(albumID) join ratesong using(songID) \
            GROUP BY songID, artist.fname, artist.lname, title, albumID, genre \
            HAVING artistName like %s"
        cursor.execute(query, ("%" + artist + "%"))

    elif not artist and genre and not rating:
        query = "SELECT song.title as title, concat(fname, ' ', lname) AS artistName, album.title as albumTitle, avg(stars) as avgrating, songID, genre \
            FROM ((((song NATURAL JOIN artistperformssong) NATURAL JOIN artist) NATURAL JOIN songgenre) NATURAL JOIN songinalbum) join album using(albumID) join ratesong using(songID) \
            GROUP BY songID, artist.fname, artist.lname, title, albumID, genre \
            HAVING genre = %s"
        cursor.execute(query, (genre))

    elif not artist and not genre and rating:
        query = "SELECT song.title as title, concat(fname, ' ', lname) AS artistName, album.title as albumTitle, avg(stars) as avgrating, songID, genre \
            FROM ((((song NATURAL JOIN artistperformssong) NATURAL JOIN artist) NATURAL JOIN songgenre) NATURAL JOIN songinalbum) join album using(albumID) join ratesong using(songID) \
            GROUP BY songID, artist.fname, artist.lname, title, albumID, genre \
            HAVING avg(stars) >= %s"
        cursor.execute(query, (rating))

    elif artist and genre and not rating:
        query = "SELECT song.title as title, concat(fname, ' ', lname) AS artistName, album.title as albumTitle, avg(stars) as avgrating, songID, genre \
            FROM ((((song NATURAL JOIN artistperformssong) NATURAL JOIN artist) NATURAL JOIN songgenre) NATURAL JOIN songinalbum) join album using(albumID) join ratesong using(songID) \
            GROUP BY songID, artist.fname, artist.lname, title, albumID, genre \
            HAVING artistName like %s and genre = %s"
        cursor.execute(query, ("%" + artist + "%", genre))

    elif artist and not genre and rating:
        query = "SELECT song.title as title, concat(fname, ' ', lname) AS artistName, album.title as albumTitle, avg(stars) as avgrating, songID, genre \
            FROM ((((song NATURAL JOIN artistperformssong) NATURAL JOIN artist) NATURAL JOIN songgenre) NATURAL JOIN songinalbum) join album using(albumID) join ratesong using(songID) \
            GROUP BY songID, artist.fname, artist.lname, title, albumID, genre \
            HAVING artistName like %s and rating >= %s"
        cursor.execute(query, ("%" + artist + "%", rating))

    elif not artist and genre and rating:
        query = "SELECT song.title as title, concat(fname, ' ', lname) AS artistName, album.title as albumTitle, avg(stars) as avgrating, songID, genre \
            FROM ((((song NATURAL JOIN artistperformssong) NATURAL JOIN artist) NATURAL JOIN songgenre) NATURAL JOIN songinalbum) join album using(albumID) join ratesong using(songID) \
            GROUP BY songID, artist.fname, artist.lname, title, albumID, genre \
            HAVING genre = %s and rating >= %s"
        cursor.execute(query, (genre, rating))

    elif artist and genre and rating:
        query = "SELECT song.title as title, concat(fname, ' ', lname) AS artistName, album.title as albumTitle, avg(stars) as avgrating, songID, genre \
            FROM ((((song NATURAL JOIN artistperformssong) NATURAL JOIN artist) NATURAL JOIN songgenre) NATURAL JOIN songinalbum) join album using(albumID) join ratesong using(songID) \
            GROUP BY songID, artist.fname, artist.lname, title, albumID, genre \
            HAVING artistName like %s and genre = %s and avg(stars) >= %s"
        cursor.execute(query, ("%" + artist + "%", genre, rating))

    else:
        if "username" in session:
            return home(error="Invalid Search")
        else:
            return render_template("index.html", error="Invalid Search")

    # stores the results in a variable
    data = cursor.fetchall()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    return render_template("songSearch.html", song_list=data, error=error)


# Define route for login
@app.route("/login")
def login():
    return render_template("login.html")


# Define route for register
@app.route("/register")
def register():
    return render_template("register.html")


# Authenticates the login
@app.route("/loginAuth", methods=["GET", "POST"])
def loginAuth():
    # grabs information from the forms
    username = request.form["username"]
    password = request.form["password"].encode("utf-8")

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = "SELECT pwd FROM user WHERE username = %s"
    cursor.execute(query, (username))
    # stores the results in a variable
    hashedPW = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if bcrypt.checkpw(password, hashedPW["pwd"].encode("utf-8")):
        # creates a session for the the user
        # session is a built in
        session["username"] = username
        return redirect(url_for("home"))
    else:
        # returns an error message to the html page
        error = "Invalid login or username"
        return render_template("login.html", error=error)


# Authenticates the register
@app.route("/registerAuth", methods=["GET", "POST"])
def registerAuth():
    # grabs information from the forms
    username = request.form["username"]
    password = request.form["password"].encode("utf-8")
    fname = request.form["fname"]
    lname = request.form["lname"]
    nickname = request.form["nickname"]

    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = "SELECT * FROM user WHERE username = %s"
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if data:
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template("register.html", error=error)
    else:
        ins = "INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s)"
        cursor.execute(ins, (username, hashed, fname, lname, date.today(), nickname))
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
        query1 = " SET @myvar = %s;"
        query2 = "\
            (select username, albumID, null as songID, title, reviewText, reviewDate \
            from reviewAlbum join album using(albumID)\
            where username = @myvar AND reviewDate > \
                (select lastlogin \
                from user \
                where username = @myvar) \
            AND \
                username in (\
                    select F.user2 as username\
                    from friend as F\
                    where F.user1 = @myvar and F.acceptStatus = 'Accepted' \
                UNION distinct\
                    select S.user1 as username\
                    from friend as S\
                    where S.user2 = @myvar and S.acceptStatus = 'Accepted') \
                OR username in\
                (select follows as username\
                from follows\
                where follower = @myvar))\
        UNION\
            (select username, null as albumID, songID, title, reviewText, reviewDate\
            from reviewSong join song using(songID)\
            where username = @myvar AND reviewDate >\
                (select lastlogin\
                from user\
                where username = @myvar) \
            AND\
                username in (\
                    select F.user2 as username \
                    from friend as F\
                    where F.user1 = @myvar and F.acceptStatus = 'Accepted' \
                UNION distinct\
                    select S.user1 as username\
                    from friend as S\
                    where S.user2 = @myvar and S.acceptStatus = 'Accepted') \
                OR username in\
                    (select follows as FollowedUsers\
                    from follows\
                    where follower = @myvar));"
        cursor.execute(query1, (user))
        data1 = cursor.fetchone()
        cursor.execute(query2, (data1))
        data2 = cursor.fetchall()
        query3 = "SELECT concat(artist.fname, ' ', artist.lname) AS artistName, songID, title\
            FROM ((((user NATURAL JOIN userfanofartist) NATURAL JOIN artistperformssong) NATURAL JOIN song ) JOIN artist using(artistID))\
            WHERE username = %s and releaseDate > lastlogin"
        cursor.execute(query3, (user))
        data3 = cursor.fetchall()
        query4 = "SELECT fname, lname FROM user WHERE username = %s"
        cursor.execute(query4, (user))
        data4 = cursor.fetchone()
        cursor.close()
        return render_template(
            "home.html",
            username=user,
            reviews=data2,
            newsongs=data3,
            realname=data4,
            error=error,
        )


@app.route("/select_song/<songID>", methods=["GET", "POST"])
def select_song(songID, error=None):
    # username = session["username"]
    cursor = conn.cursor()
    query1 = "SELECT songID, song.title as title, concat(artist.fname, ' ', artist.lname) AS artistName, genre, releaseDate, songURL, album.title as albumTitle, avg(stars) as averageRating, artistID \
        FROM (((((song natural join songgenre) natural join artistperformssong) join artist using(artistID)) natural join songinalbum) join album using(albumID) )join ratesong using(songID)\
        GROUP BY songID, title, artistName, genre, releaseDate, songURL, albumTitle, artistID \
        HAVING songID = %s "

    cursor.execute(query1, songID)
    songdata = cursor.fetchall()

    query2 = "SELECT * FROM reviewsong WHERE songID = %s"
    cursor.execute(query2, songID)
    reviews = cursor.fetchall()
    cursor.close()
    return render_template(
        "select_song.html", song_info=songdata, reviews=reviews, error=error
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
    username = session["username"]
    cursor = conn.cursor()
    query0 = " SET @myvar = %s;"
    query = "select F.user2 as username \
		from friend as F \
		where F.user1 = @myvar and F.acceptStatus = 'Accepted'  \
		UNION distinct \
		select S.user1 as username \
		from friend as S \
		where S.user2 = @myvar and S.acceptStatus = 'Accepted'"
    cursor.execute(query0, (username))
    placeholder = cursor.fetchall()
    cursor.execute(query, (placeholder))
    data = cursor.fetchall()
    cursor.close()
    return render_template("curr_friends.html", username=username, friendlist=data)


@app.route("/pending_requests")
def pending_requests():
    username = session["username"]
    cursor = conn.cursor()
    query0 = " SET @myvar = %s;"
    query = "select user1 as requester \
	    from friend \
	    where user2 = @myvar and acceptStatus = 'Pending' and requestSentBy = user1 \
	    UNION \
	    select user2 as requester \
	    from friend \
	    where user1 = @myvar and acceptStatus = 'Pending' and requestSentBy = user2"
    cursor.execute(query0, (username))
    placeholder = cursor.fetchall()
    cursor.execute(query, (placeholder))
    data = cursor.fetchall()
    cursor.close()
    return render_template("pending_requests.html", username=username, requests=data)


@app.route("/accept_req/<user>")
def accept_req(user):
    username = session["username"]
    cursor = conn.cursor()
    query = "UPDATE friend SET acceptStatus = 'Accepted' WHERE (user1 = %s AND user2 = %s) OR (user2 = %s AND user1 = %s)"
    cursor.execute(query, (username, user, username, user))
    conn.commit()
    cursor.close()
    return redirect(url_for("pending_requests"))


@app.route("/deny_req/<user>")
def deny_req(user):
    username = session["username"]
    cursor = conn.cursor()
    query = "UPDATE friend SET acceptStatus = 'Not Accepted' WHERE (user1 = %s AND user2 = %s) OR (user2 = %s AND user1 = %s)"
    cursor.execute(query, (username, user, username, user))
    conn.commit()
    cursor.close()
    return redirect(url_for("pending_requests"))


@app.route("/search_users")
def search_users():
    username = session["username"]
    friend = request.args["user"]
    cursor = conn.cursor()
    query = "SELECT username, concat(fname, ' ', lname) as name FROM user WHERE (username like %s OR concat(fname, ' ', lname) like %s) and username <> %s"
    cursor.execute(query, ("%" + friend + "%", "%" + friend + "%", username))
    data = cursor.fetchall()
    if data:
        return render_template("searched_users.html", result=data)
    else:
        error = "No users found"
        return home(error)


@app.route("/follow/<person>")
def follow(person):
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
    username = session["username"]
    cursor = conn.cursor()

    query = "select artistID, concat(fname, ' ', lname) AS artistName, artistBio, artistURL\
		from userfanofartist NATURAL JOIN artist \
		where username = %s"

    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    return render_template("followed_artists.html", username=username, artistList=data)


@app.route("/artist/<artistID>")
def artist(artistID, error=None):
    cursor = conn.cursor()
    songQuery = "SELECT songID, title, releaseDate, genre, avg(stars) AS averageRating FROM artistperformssong NATURAL JOIN song NATURAL JOIN songgenre NATURAL JOIN ratesong GROUP BY songID, title, releaseDate, genre, artistID HAVING artistID = %s"
    cursor.execute(songQuery, (artistID))
    songResults = cursor.fetchall()

    albumQuery = "SELECT albumID, album.title as title, avg(stars) AS averageRating FROM artistperformssong NATURAL JOIN song NATURAL JOIN songinalbum JOIN album using(albumID) NATURAL JOIN ratealbum GROUP BY albumID, title, artistID HAVING artistID = %s"
    cursor.execute(albumQuery, (artistID))
    albumResults = cursor.fetchall()

    artistQuery = "SELECT concat(fname, ' ', lname) AS artistName, artistBio, artistURL, artistID FROM artist WHERE artistID=%s"
    cursor.execute(artistQuery, (artistID))
    artistResults = cursor.fetchall()

    cursor.close()
    return render_template(
        "artist.html",
        songResults=songResults,
        albumResults=albumResults,
        artistResults=artistResults,
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
    username = session["username"]
    search = request.args["search"]
    cursor = conn.cursor()
    query = "SELECT artistID, concat(fname, ' ', lname) AS artistName FROM artist WHERE artistID like %s OR concat(fname, ' ', lname) like %s"
    cursor.execute(query, ("%" + search + "%", "%" + search + "%"))
    data = cursor.fetchall()
    if data:
        return render_template("searched_artists.html", result=data)
    else:
        error = "No artists found"
        return home(error)


@app.route("/user/<user>")
def user(user, error=None):
    username = session["username"]  # must be logged in
    cursor = conn.cursor()
    userQuery = "SELECT username, concat(fname, ' ', lname) as name, lastlogin, nickname FROM user WHERE username = %s"
    cursor.execute(userQuery, (user))
    userInfo = cursor.fetchall()

    artistQuery = "SELECT artistID, concat(fname, ' ', lname) as artistName, artistBio, artistURL FROM userfanofartist NATURAL JOIN artist WHERE username = %s"
    cursor.execute(artistQuery, (user))
    artistResults = cursor.fetchall()

    songRatingQuery = "SELECT songID, stars, ratingDate, title, concat(artist.fname, ' ', artist.lname) AS artistName, artistID FROM ratesong NATURAL JOIN song NATURAL JOIN artistperformssong JOIN artist using(artistID) WHERE username = %s"
    cursor.execute(songRatingQuery, (user))
    songRatings = cursor.fetchall()

    songReviewQuery = "SELECT songID, reviewText, reviewDate, title, concat(artist.fname, ' ', artist.lname) AS artistName, artistID FROM reviewsong NATURAL JOIN song NATURAL JOIN artistperformssong JOIN artist using(artistID) WHERE username = %s"
    cursor.execute(songReviewQuery, (user))
    songReviews = cursor.fetchall()

    albumRatingQuery = "SELECT albumID, stars, title, concat(artist.fname, ' ', artist.lname) AS artistName, artistID FROM ratealbum NATURAL JOIN album NATURAL JOIN songinalbum NATURAL JOIN artistperformssong JOIN artist using(artistID) WHERE username = %s"
    cursor.execute(albumRatingQuery, user)
    albumRatings = cursor.fetchall()

    albumReviewQuery = "SELECT albumID, reviewText, reviewDate, album.title as albumTitle, concat(artist.fname, ' ', artist.lname) AS artistName, artistID FROM reviewalbum NATURAL JOIN album NATURAL JOIN songinalbum NATURAL JOIN artistperformssong JOIN artist using(artistID) WHERE username = %s"
    cursor.execute(albumReviewQuery, user)
    albumReviews = cursor.fetchall()

    cursor.close()
    return render_template(
        "user.html",
        userInfo=userInfo,
        artistResults=artistResults,
        songRatings=songRatings,
        songReviews=songReviews,
        albumRatings=albumRatings,
        albumReviews=albumReviews,
        error=error,
    )


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def upload_form():
    return render_template("upload.html")


@app.route("/", methods=["POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No file selected for uploading")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            flash("File successfully uploaded")
            return redirect("/")
        else:
            flash("Allowed file types are txt, pdf, png, jpg, jpeg, gif")
            return redirect(request.url)


@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")


app.secret_key = "some key that you will never guess"
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
