from unittest import TestCase
from app import app
from flask import session
from models import db, connect_db, User

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_tests'

db.drop_all()
db.create_all()

class UserTests(TestCase):

    def setUp(self):
        self.client = app.test_client()

        User.query.delete()

        new_user = User(first_name="Jessica", last_name="Lee")
        db.session.add(new_user)
        db.session.commit()
        self.user_id = new_user.id
      
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

            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects=True) 
            html = resp.get_data(as_text=True)      

            self.assertNotIn('Jessica Lee', html)

    def test_show_details_deleted_user(self):
        with self.client as client:
            id = self.user_id

            delete_person = client.post(f'/users/{id}/delete', follow_redirects=True) 

            resp = client.get(f'/users/{id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 404)              

    def test_edit_user_form_populates(self):
        with self.client as client:

            resp = client.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jessica', html)
            self.assertIn('Lee', html)

    def test_edit_user_details(self):
        with self.client as client:

            resp = client.post(f'/users/{self.user_id}/edit', data={'first-name': 'Paige', 'last-name': 'Godfrey'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Paige Godfrey', html)
            self.assertNotIn('Jessica Lee', html)   