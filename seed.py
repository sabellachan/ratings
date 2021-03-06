"""Utility file to seed ratings database from MovieLens data in seed_data/"""


from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app
import datetime


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

    Movie.query.delete()

    for row in open("seed_data/u.item"):
        row = row.rstrip()
        row = row.split('|')
        if row != []:
            movie_id = row[0]
            full_title = row[1].split('(')
            title = full_title[0].rstrip()
          
            if row[2] != '':
                released_at = datetime.datetime.strptime(row[2], "%d-%b-%Y")
            else:
                released_at = None
            imdb_url = row[4]
          
            movie = Movie(movie_id=movie_id, 
                            title=title,
                            released_at=released_at,
                            imdb_url=imdb_url)

            db.session.add(movie)

    db.session.commit()


    #     movie_id INTEGER NOT NULL, 
    # title VARCHAR(64) NOT NULL, 
    # released_at DATETIME, 
    # imdb_url VARCHAR(64), 
    # PRIMARY KEY (movie_id)



def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    Rating.query.delete()

    for row in open("seed_data/u.data"):
        row = row.strip()
        user_id, movie_id, score, timestamp = row.split()

        rating = Rating(user_id=user_id,
                         movie_id=movie_id,
                         score=score)

        db.session.add(rating)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
