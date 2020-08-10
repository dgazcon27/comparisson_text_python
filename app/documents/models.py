from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError
from app import db
from os.path import join
from io import StringIO
import re
from app import upload_folder

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from nltk import ngrams


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
        folder = upload_folder
        document = join(folder, self.title)
        text_process = self.get_text_from_pdf(document)
        # Getting list of documents stored
        documents_list = Document.query.filter(Document.title != self.title).all()
        # docs_pro = self.get_text_from_pdf(join(folder, docs.title))
        # Check documents using ngram method
        result_ngram = self.compare_ngram(text_process, documents_list)
        print(result_ngram)
        return None

    def compare_ngram(self, doc_up, list_store_doc, n=3):
        folder = upload_folder
        tgram_up = list(ngrams(doc_up, n))
        list_result = []
        list_merge = []
        for doc in list_store_doc:
            docs_pro = self.get_text_from_pdf(join(folder, doc.title))
            doc_tgram = list(ngrams(docs_pro, n))
            common = []
            for gram in tgram_up:
                if gram in doc_tgram:
                    common.append(gram)
            if len(common) > 0:
                uniq_gram = self.remove_duplicate(common)
                total_grams = self.remove_duplicate(tgram_up+doc_tgram)
                total_result = '{:.4f}'.format((len(uniq_gram)/len(total_grams))*100)
                list_result.append({"ngram": total_result, "suspect": doc.id, "name": doc.title})
        return list_result

    def remove_duplicate(self, list_of_item):
        unique = list(dict.fromkeys(list_of_item))
        return unique

    def print_list(self, list3):
        for x in list3:
            print(x)
        print("\n")

    def merge_ngrams(self, list1, list2):
        for item in list2:
            list1.append(item2)
        # for item in list1:
        #     if item not in list2:
        #         list_items.append(item)
        return list1

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

    
