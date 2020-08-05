from flask import abort, render_template
from . import public_bp
from flask_login import login_required, current_user

@public_bp.route("/")
@login_required
def index():
    return render_template("index.html")
