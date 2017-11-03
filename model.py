"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
import correlation

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True, unique=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Displays info"""

        return ("<User user_id={} email={} password={} age={} zipcode={}>".format(self.user_id, self.email, self.password, self.age, self.zipcode))

    def similarity(self, other_user):
        """Return Pearson rating for user compared to other user."""

        curr_user_ratings = {}
        paired_ratings = []

        for r in self.ratings:
            curr_user_ratings[r.movie_id] = r

        # For every movie in someone else's rating list, find if you
        # also have rated that movie. If you do: append your data
        # to the tuple thingy.
        for o_r in other_user.ratings:
            curr_user_r = curr_user_ratings.get(o_r.movie_id)

            # If current user has rated this movie
            if curr_user_r:
                paired_ratings.append((curr_user_r.score, o_r.score))

        if paired_ratings:
            return correlation.pearson(paired_ratings)

        # If there was no overlap in movies rated
        else:
            return 0.0

# Put your Movie and Rating model classes here.


class Rating(db.Model):
    """Rating information."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('ratings', order_by=rating_id))
    movie = db.relationship('Movie', backref=db.backref('ratings', order_by=rating_id))


class Movie(db.Model):
    """ Movie information."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)
    imdb_url = db.Column(db.String(255), nullable=True)

    # ratings = db.relationship('Rating')


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
