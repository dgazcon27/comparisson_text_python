from flask import Flask,render_template, request, redirect, url_for
from forms import LoginForm, DocumentForm
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from os.path import abspath, dirname, join
import os

BASE_DIR = dirname(dirname(abspath(__file__)))


app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/sis_plag'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = join(BASE_DIR, 'path/upload')


login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)

from model.User import User
from model.Post import Post
from model.Document import Document


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = DocumentForm()
    error = None
    if form.validate_on_submit():
        file = form.upload.data
        if file:
            image_name = secure_filename(file.filename)
            images_dir = app.config['UPLOAD_FOLDER']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            file.save(file_path)
            document = Document(user_id=current_user.id, title= image_name)
            document.save()
            doc_uploaded = document.get_stats_coincidence()
            
            return redirect(url_for('index'))
    return render_template("admin/upload_form.html", form=form)    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))