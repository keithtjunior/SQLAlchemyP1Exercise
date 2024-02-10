from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class AppTests(TestCase):
    
    def setUp(self):
        """Add test user"""
        User.query.delete()
        user = User(first_name='Test', last_name='User', img_url='')
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

    def tearDown(self):
        """Clean up transactions"""
        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            res = client.get('/')
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/users')

    def test_list_users(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<div class="list-group">', html)

    def test_show_user(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<p class="card-text">User Info...</p>', html)

    def test_create_user(self):
        with app.test_client() as client:
            data = {
                "first-name": "New", 
                "last-name": "User", 
                "img-url": 'https://upload.wikimedia.org/wikipedia/commons/1/1e/Default-avatar.jpg'
                }
            res = client.post('/users/new', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_update_user(self):
        with app.test_client() as client:
            data = {
                "first-name": "New", 
                "last-name": "Update", 
                "img-url": 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png'
                }
            res = client.post(f'/users/{self.user_id}/edit', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)