from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError
from run import db, app
from os.path import join
from io import StringIO
import re

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser



class Document(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(256), nullable=False)

    def save(self):
        if not self.id:
            db.session.add(self)

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                count += 1
                self.title = f'{self.title}-{count}'

    def get_by_title(self):
        return Document.query.filter_by(title=self.title).first()

    def get_stats_coincidence(self):
        upload_folder = app.config['UPLOAD_FOLDER']
        document = join(upload_folder, self.title)
        text_process = self.get_text_from_pdf(document)
        print(text_process)
        # documents_list = Document.query.filter(Document.title != self.title).all()
        # for docs in documents_list:
        #     doc_list_process = 
        return None

    def get_text_from_pdf(self, url):
        regex = r"/\t|\n|\/|\,|\.|\:|\;|\(|\)|\{|\}|\?|\¿|\"|\'|\_|\-|\]|\[/g"
        process_text = None
        output_string = StringIO()
        with open(url, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
        process_text = output_string.getvalue()
        if len(process_text) > 0:
            process_text = process_text.lower()
            process_text = re.sub(regex,"", process_text)
            process_text = re.sub(r'\d+', '', process_text)
            process_text = re.split("  *", process_text)
        return process_text
