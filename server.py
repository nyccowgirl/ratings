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

@app.route("/users")
def user_list():
    """ Displays list of users by email and user_id). """

    users = User.query.all()

    return render_template('user_view.html', jinja_user=users)

@app.route("/login")
def display_signin():
    """ Displays login form. """

    return render_template('login.html')


@app.route("/registration", methods=["POST"])
def register():
    """ Registers user """

    form_email = request.form.get('form_email')
    form_pw = request.form.get('form_pw')
    form_zip = request.form.get('form_zip')
    form_age = request.form.get('form_age')
    # return render_template('login.html')

    db.session.add(User(email=form_email, password=form_pw, age=form_age, zipcode=form_zip))
    db.session.commit()

    session['email'] = form_email

    flash('Registration confirmed!')

    return redirect("/")


@app.route("/register", methods=['GET'])
def check_signin():
    """ Checks email from login form. """

    form_email = request.args.get('form_email')
    form_pw = request.args.get('form_pw')

    user = User.query.filter_by(email=form_email).first()
    if user is None:
        print "\n\n\n OBSCENICORN \n\n\n"
        flash("You are not registered. Register now!")
        return render_template("registration_form.html")
    elif (user.email == form_email) and (user.password == form_pw):
        session['email'] = form_email
        flash('You are logged in!')
        print "\n\n\n"
        print user.email, user.password
        print "\n\n\n"
        return redirect("/")
    else:
        flash('Wrong password, dummy! Try again')
        return redirect("/login")


    # if user is None:
    #     #sign in and redirect to homepage
    #     return redirect('/registration', methods=['POST'])
    # else:
    #     # add to DB and commit
    #     # return render_template('registration_form.html')
    #     return redirect('/')
    #     print "USER EXISTS"



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
