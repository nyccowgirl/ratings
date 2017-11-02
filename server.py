"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session, flash)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined  


@app.route('/')
def index():
    """Homepage."""
    # a = jsonify([1,3])
    # return a
    return render_template("homepage.html")


@app.route('/logout')
def logout():
    """ Logs user out """

    # need to add a button and some dynamic javascript here to
    # change to login
    session.clear()

    flash("You are logged out. Congrats!")

    return redirect("/")


@app.route("/users")
def user_list():
    """ Displays list of users by email and user_id). """

    users = User.query.order_by(email=session['email']).all()

    return render_template('user_view.html', jinja_user=users)


@app.route("/user_profile")
def user_profile():
    """ Displays user information including movies that were rated. """

    user = User.query.filter_by(email=session['email']).first()
    ratings = user.ratings
    movies = []

    for rating_ob in ratings:
        title = Movie.query.filter_by(movie_id=rating_ob.movie_id).first().title
        movies.append((title,rating_ob.score))

    return render_template('user.html', jinja_user=user, jinja_movies=movies)


@app.route("/movies")
def movie_list():
    """ Displays list of movies. """

    movies = Movie.query.order_by(title).all()

    return render_template('movie_view.html', jinja_movies=movies)


@app.route("/login", methods=['GET'])
def display_signin():
    """ Displays login form. """

    return render_template('login.html')


@app.route("/login", methods=['POST'])
def log_in():
    """ Logs in user. """

    form_email = request.form.get('form_email')
    form_pw = request.form.get('form_pw')

    user = User.query.filter_by(email=form_email).first()

    if user is None:
        flash("You are not registered. Register now!")
        return redirect("/register")
    elif (user.email == form_email) and (user.password == form_pw):
        session['email'] = form_email
        print session
        flash('You are logged in as {}!'.format(session['email']))
        print "\n\n\n"
        print user.email, user.password
        print "\n\n\n"
        return redirect("/user_profile")
    else:
        flash('Wrong password, dummy! Try again')
        return redirect("/login")


@app.route("/register", methods=["POST"])
def register():
    """ Registers user """

    print "\n\n\nbefore registration submission", session
    form_email = request.form.get('form_email')
    form_pw = request.form.get('form_pw')
    form_zip = request.form.get('form_zip')
    form_age = request.form.get('form_age')
    # return render_template('login.html')

    user = User.query.filter_by(email=form_email).first()

    if user is None:
        db.session.add(User(email=form_email, password=form_pw, age=form_age, zipcode=form_zip))
        db.session.commit()
        session['email'] = form_email
        # user = User.query.filter_by(email=form_email).first()
        return redirect("/user_profile")
    # elif (user.email == form_email) and (user.password == form_pw):
    #     flash('You are already in our system and logged in as {}!'.format(session['email']))
    #     return redirect("/user_profile")
    else:
        flash('You are already in our system, please log in.')
        return redirect("/login")



    print "\n\n\nbefore cookie initiated", session
    session['email'] = form_email
    print "\n\n\nafter",session

    flash('Registration confirmed!')

    return redirect("/")


@app.route("/register", methods=['GET'])
def check_signin():
    """ Checks email from login form. """

    return render_template("registration_form.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')  # Good thing to put into your code
