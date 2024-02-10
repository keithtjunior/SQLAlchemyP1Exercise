"""Blogly application."""

from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = 'heartthrobnever1978'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home():
    # app.logger.info('variable: %s', variable)
    # import pdb;  pdb.set_trace()
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user-listing.html', users=users)

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("user-detail.html", user=user)

@app.route('/users/new', methods=["GET"])
def new_user():
    """Create a new user form"""
    return render_template('user-create.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Create a new user"""
    first_name = request.form["first-name"].strip()
    last_name = request.form["last-name"].strip()
    img_url = request.form["img-url"].strip()
    img_url = img_url if img_url else None
    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/edit/', methods=["GET"])
def edit_user(user_id):
    """Edit a user's information"""
    user = User.query.get_or_404(user_id)
    return render_template('user-edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Update a user's information"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first-name"].strip()
    user.last_name = request.form["last-name"].strip()
    img_url = request.form["img-url"].strip()
    user.img_url = img_url if img_url else None
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')