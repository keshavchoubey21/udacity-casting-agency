import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database.models import setup_db, Movie, Actor
from flask_cors import CORS, cross_origin
from app import app

class CastingAgency(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = "postgresql://postgres:hazard@localhost:5432/realtodoapp"
        setup_db(self.app)

        self.new_movie = {
            'title': 'test movie',
            'releaseDate': '1977-05-05'
        }

        self.new_actor = {
            'name': 'test actor',
            'age': 40,
            'gender': 'F'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    # get apis

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # create apis

    def test_create_actor(self):
        res = self.client().post('/actor', json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # delete apis

    def test_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(res.status_code, 200)

    def test_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(res.status_code, 200)
    
    # error scenario

    def test_404_no_movies(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_404_no_actors(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

if __name__ == "__main__":
    unittest.main()