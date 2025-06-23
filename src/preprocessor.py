# src/preprocessor.py

import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import os

class Preprocessor:
    def __init__(self):
        pass

    def process_url(self, url: str) -> str:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator='\n')
        return self.clean_text(text)

    def process_pdf(self, pdf_path: str) -> str:
        doc = fitz.open(pdf_path)
        texts = [page.get_text() for page in doc]
        return self.clean_text("\n".join(texts))

    def process_txt(self, txt_path: str) -> str:
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return self.clean_text(text)

    def clean_text(self, text: str) -> str:
        lines = text.splitlines()
        return "\n".join([line.strip() for line in lines if line.strip()])