"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User, Movie, Rating
# from model import Rating
# from model import Movie
from datetime import datetime

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print "Movies"

    # To delete tables each time we open up a session.
    Movie.query.delete()

    for row in open('seed_data/u.item'):
        row = row.rstrip()  # removes whitespace, but still a long string
        row = row.split('|')
        movie_id, title, release_date, video_date, imdb = row[:5]
        # movie_id = row[0]
        # title = row[1]
        # release_date = row[2]
        # imdb = row[3]

        if release_date:
            release_date = datetime.strptime(release_date, '%d-%b-%Y')
        else:
            release_date = None

        title = title[:-7] # (\d{4})$ regex (import re library)
        print imdb
        movie = Movie(movie_id=movie_id,
                      title=title,
                      released_at=release_date,
                      imdb_url=imdb)

        # to add to database for each movie
        db.session.add(movie)

    # to show that we do not have a fear of committing
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    Rating.query.delete()

    for row in open('seed_data/u.data'):
        row = row.rstrip()
        user_id, movie_id, score, timestamp = row.split('\t')

        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)

        db.session.add(rating)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
