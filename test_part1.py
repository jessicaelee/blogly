from unittest import TestCase
from app import app
from flask import session

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class UserTests(TestCase):

    def test_root_redirection(self):
          with app.test_client() as client:

            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1> Users </h1>', html)

    def test_show_added_user(self):
          with app.test_client() as client:

            resp = client.post('/users/new', 
                            data={'first-name': 'test_first', 'last-name': 'test_last'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/users/10">test_first test_last</a>', html)

    def test_check_deleted_user(self):
        with app.test_client() as client:

            resp = client.post('/users/<int:user_id>/delete', follow_redirects=True)

             

