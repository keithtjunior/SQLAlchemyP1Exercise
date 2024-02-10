"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(70), nullable=False)
    last_name = db.Column(db.String(70), nullable=False)
    img_url = db.Column(
                db.String(2048), 
                nullable=False,
                default='https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png'
            )
    
    def __repr__(self):
        u = self
        return f'<User id={u.id} first_name={u.first_name} last_name={u.last_name} img_url={u.img_url}>'
    
    def get_full_name(self):
        """Return full name"""
        return f'{self.first_name} {self.last_name}'
    
    full_name = property(fget=get_full_name)
