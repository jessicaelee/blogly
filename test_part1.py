from unittest import TestCase
from app import app
from flask import session
from models import db, connect_db, User

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

class UserTests(TestCase):

    def setUp(self):
      self.client = app.test_client()
      User.query.delete() #FIX THIS - TABLE ISN'T WORKING PROPERLY
      db.session.commit()
      
    def test_root_redirection(self):
          with self.client as client:

            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1> Users </h1>', html)

    def test_show_added_user(self):
          with self.client as client:

            resp = client.post('/users/new', 
                            data={'first-name': 'test_first', 'last-name': 'test_last'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_first test_last', html)

    def test_check_deleted_user(self):
        with self.client as client:

            create_user = client.post('/users/new', 
                            data={'first-name': 'delete_first', 'last-name': 'delete_last'}, follow_redirects=True)

            resp = client.post('/users/34/delete', follow_redirects=True) #FIX NUMBER/ID REFERENCE 
            html = resp.get_data(as_text=True)      

            self.assertNotIn('delete_first delete_last', html)

            # import pdb; pdb.set_trace()
