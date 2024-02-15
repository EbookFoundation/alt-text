#This file will be the actual generation of images and benchmarking of the system

#Run getbooks.py then downloadbooks.py with whatever .txt is being used then use those to move into the next steps
import os
import bs4
from bs4 import BeautifulSoup
import time
from ..src.alttext.alttext import getImgData, getContext, genDesc, genChars
from ..src.alttext.langengine import refineAlt

class BookParser:
    def __init__(self):
        self.filepath = ""
        self.filename = ""
        self.filedir = ""

    def parse(self, html):
        # Parse the HTML content with BeautifulSoup
        return BeautifulSoup(html, 'html.parser')

    def parseFile(self, filepath: str) -> bs4.BeautifulSoup:
        with open(filepath, encoding="utf8") as html:
            self.filepath = filepath
            l = filepath.split("/")
            self.filename = l.pop()
            self.filedir = "/".join(l) + "/"
            return self.parse(html)

def process_books(extraction_folder):
    parser = BookParser()

    # Iterate through each book's directory
    for book_id in os.listdir(extraction_folder):
        book_path = os.path.join(extraction_folder, book_id)
        if os.path.isdir(book_path):
            # Iterate through files in the book's directory
            for filename in os.listdir(book_path):
                filepath = os.path.join(book_path, filename)
                # Check if the file is an HTML file
                if filepath.endswith(".html"):
                    # Use the parseFile method to parse the HTML file
                    soup = parser.parseFile(filepath)
                    # Now `soup` contains the parsed HTML file for further processing

                    # Example of further processing: print the title of the HTML document
                    title = soup.find('title').get_text() if soup.find('title') else 'No title'
                    print(f"Book ID: {book_id}, File: {filename}, Title: {title}")

#Use genAltTextV2
#ADD benchmark time stamps
def genAltTextV2(self, src: str) -> str:
        imgdata = self.getImgData(src)
        context = [None, None]
        if self.options["withContext"]:
            context = self.getContext(self.getImg(src))
        desc = self.genDesc(imgdata, src, context)

        chars = ""
        if self.ocrEngine != None:
            chars = self.genChars(imgdata, src).strip()

        if self.langEngine == None:
            raise Exception("To use version 2, you must have a langEngine set.")

        return self.langEngine.refineAlt(desc, chars, context, None)

#Add .csv generation for benchmark variables