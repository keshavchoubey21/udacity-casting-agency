import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, Movie, Actor, setup_db
from .auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
app.app_context().push()

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

'''
MOVIES
'''

@app.route("/movies", methods=["GET"])
def get_movies():
        try:    
            movies = Movie.query.all()
            if len(movies) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "movies": movies
                    
                },200)
        except:
            abort(404)


@app.route('/movies', methods=["POST"])
@requires_auth("post:movies")
def post_movies(payload):
    body = request.get_json()
    new_title = body.get('title', None)
    new_releaseDate = body.get('releaseDate', None)

    try:
        movie = Movie(title=new_title, releaseDate=new_releaseDate)
        movie.insert()

        return jsonify({
            'success': True,
            'movies': movie.format(),
            'created': movie.id
        })
    except:
        abort(422)

@app.route('/movies/<int:movie_id>', methods=["DELETE"])
@requires_auth("delete:movies")
def delete_movie(movie_id):

    try:
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        movie.delete()
        return jsonify(
            {
                "success": True,
                "delete": movie_id
            },
        200)
    except:
        abort(422)

@app.route('/movies/<int:movie_id>', methods=["PATCH"])
@requires_auth("patch:movies")
def update_drink(payload,movie_id):

    body = request.get_json()

    try:
        movie = Movie.query.get(movie_id)

        if movie is None:
            abort(404)
        if 'title' in body:
            movie.title = body.get('title', None)
        if 'releaseDate' in body:
            movie.releaseDate = body.get('releaseDate', None)

        movie.insert()

        return jsonify({
            'success': True,
            'movies': movie.format()
        })
    except:
        abort(422)

'''
ACTORS
'''

@app.route("/actors", methods=["GET"])
def get_actors():
        try:    
            actors = Actor.query.all()
            if len(actors) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "movies": actors
                    
                },200)
        except:
            abort(404)

@app.route('/actors', methods=["POST"])
@requires_auth("post:actors")
def post_actors(payload):
    body = request.get_json()
    new_name = body.get('name', None)
    new_gender = body.get('gender', None)
    new_age = body.get('age', None)

    try:
        actor = Actor(name=new_name, gender=new_gender, age=new_age)
        actor.insert()

        return jsonify({
            'success': True,
            'actors': actor.format(),
            'created': actor.id
        })
    except:
        abort(422)

@app.route('/actors/<int:actor_id>', methods=["DELETE"])
@requires_auth("delete:actors")
def delete_actors(actor_id):

    try:
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)

        actor.delete()
        return jsonify(
            {
                "success": True,
                "delete": actor_id
            },
        200)
    except:
        abort(422)

@app.route('/actors/<int:actor_id>', methods=["PATCH"])
@requires_auth("patch:actors")
def update_drink(payload,actor_id):

    body = request.get_json()

    try:
        actor = Actor.query.get(actor_id)

        if actor is None:
            abort(404)
        if 'name' in body:
            actor.name = body.get('name', None)
        if 'age' in body:
            actor.age = body.get('age', None)
        if 'gender' in body:
            actor.gender = body.get('gender', None)

        actor.insert()

        return jsonify({
            'success': True,
            'actors': actor.format()
        })
    except:
        abort(422)


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    },422)


@app.errorhandler(422)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    },404)


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    },500)


@app.errorhandler(AuthError)
def not_found(auth_error):
    return jsonify({
        "success": False,
        "error": auth_error.status_code,
        "message": auth_error.error["description"]
    }, auth_error.status_code)
