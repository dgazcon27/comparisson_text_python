from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os.path import abspath, dirname, join

login_manager = LoginManager()
db = SQLAlchemy()
BASE_DIR = dirname(dirname(abspath(__file__)))
upload_folder = join(BASE_DIR, 'path/upload')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/sis_plag'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    db.init_app(app)

    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from .public import public_bp
    app.register_blueprint(public_bp)

    from .documents import document_bp
    app.register_blueprint(document_bp)
    
    return app