from flask import render_template, redirect, url_for
from werkzeug.utils import secure_filename
from os.path import join
import os
from flask_login import login_required, current_user

from app.documents.models import Document
from app.documents.forms import DocumentForm
from . import admin_bp
from app import upload_folder


@admin_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = DocumentForm()
    error = None
    if form.validate_on_submit():
        file = form.upload.data
        if file:
            doc_name = secure_filename(file.filename)
            docs_dir = upload_folder
            document = Document(user_id=current_user.id, title= doc_name)
            check_document = document.get_by_title()
            if check_document is None:
                document.save()
                os.makedirs(docs_dir, exist_ok=True)
                file_path = os.path.join(docs_dir, document.title)
                file.save(file_path)
                doc_uploaded = document.get_stats_coincidence()

            return redirect(url_for('public.index'))
    return render_template("admin/upload_form.html", form=form)