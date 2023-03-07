from flask import Flask, render_template, request, url_for, redirect, flash
from dict import telescopes as tel
from forms import ContactForm
import os
from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import secrets
from PIL import Image
# from werkzeug.utils import secure_filename
# from flask_login import current_user, UserMixin


SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app, db)


# Tables
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(),nullable=True, default='default.jpg')
    
    def __init__(self, name, email, message, date, image):
        self.name = name
        self.email = email
        self.message = message
        self.date = date
        self.image = image
        
    def __repr__(self):
        return f'{self.name} - {self.email}, message: {self.message}. {self.date}'
    
class HubbleCards(db.Model):
    __tablename__ = 'hubble_cards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    image = db.Column(db.Text, nullable=False)
    
    def __init__(self, name, image):
        self.name = name
        self.image = image
          
    def __repr__(self):
        return f'{self.name}, {self.image} '

@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html',  title='Homepage')
        
@app.route("/info", methods=['GET', 'POST'])
def info():
    if request.method == 'POST':
        return redirect(url_for('index.html', title='Homepage'))
    return render_template('info.html', title='Information')

@app.route("/data")
def data():
    if request.method == 'POST':
        return redirect(url_for('index.html', title='Homepage'))
    return render_template('data.html', title='Data')

@app.route("/draft")
def draft():
    return render_template('draft.html', title='Draft')

# save picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn  

@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():
    data = Message.query.all()
    form = ContactForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_picture(form.image.data)
        dateNow = datetime.now()
        dateNowFormatted = dateNow.strftime("%d/%m/%Y %H:%M:%S")
        dbEntry = Message(
                          name=form.name.data,
                          email=form.email.data,
                          message = form.body.data,
                          date = dateNowFormatted,
                          image=image_file
                          )
        db.session.add(dbEntry)
        db.session.commit()
        return render_template('contact_success.html', form=form, data=data)
    return render_template('contact_us.html', form=form, data=data, title='Contact us') 


@app.route("/contact_success")
def contact_success():
    return render_template('contact_success.html',  title='Contact Success')

@app.route("/exoplanets")
def exoplanets():
    return render_template('exoplanets.html', title='Exoplanets')

@app.route("/telescopes")
def telescopes():
    
    return render_template('telescopes.html', title='Telescopes', tel=tel)

@app.route("/methods")
def methods():
    
    return render_template('methods.html', title='Methods')

if __name__ == '__main__':
    app.run(debug=True)