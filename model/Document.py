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

    def get_text_from_pdf(self, url):
        regex = r"/\t|\n|\,|\.|\:|\;|\(|\)|\{|\}|\?|\¿|\"|\'|\_|\-|\]|\[/g"
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
            process_text = re.sub(regex,"", process_text).split(" ")
        return process_text

    def get_stats_coincidence(self):
        upload_folder = app.config['UPLOAD_FOLDER']
        document = join(upload_folder, self.title)
        x = self.get_text_from_pdf(document)

        print(x[len(x)-1])
        return None
