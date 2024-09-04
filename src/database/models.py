import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

# database_filename = "database.db"
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
database_path="postgresql://owner:QCLTD4vGQTYJJVmK4zJpGXTZhkINyu0Q@dpg-crai7cq3esus73a1ijeg-a.oregon-postgres.render.com/casting_agency_database_622a"
# database_path="postgresql://postgres:hazard@localhost:5432/realtodoapp"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    movie1 = Movie(title="The Shawshank Redemption", releaseDate="1994-09-23")
    movie2 = Movie(title="The Godfather", releaseDate="1972-03-24")

    actor1 = Actor(name="Morgan Freeman", age=83, gender="Male")
    actor2 = Actor(name="Marlon Brando", age=80, gender="Male")
    actor3 = Actor(name="Al Pacino", age=82, gender="Male")

    # Add to session
    db.session.add(movie1)
    db.session.add(movie2)
    db.session.add(actor1)
    db.session.add(actor2)
    db.session.add(actor3)

    # Commit to the database
    db.session.commit()


    # drink.insert()
# ROUTES

'''
Movie
'''

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    releaseDate = Column(db.DateTime)

    def __init__(self, title, releaseDate):
        self.title = title
        self.releaseDate = releaseDate

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'releaseDate': self.releaseDate
        }

class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age}