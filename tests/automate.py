#This file will be the actual generation of images and benchmarking of the system

#Run getbooks.py then downloadbooks.py with whatever .txt is being used then use those to move into the next steps
import os
import bs4
from bs4 import BeautifulSoup
import time
from ..src.alttext.alttext import getImgData, getContext, genDesc, genChars
from ..src.alttext.langengine import refineAlt
import csv

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

class AltTextGenerator:
    def __init__(self):
        self.benchmark_records = []

    #Use genAltTextV2
    #ADD benchmark time stamps
    def genAltTextV2(self, src: str) -> str:
        # Start total timing
        total_start_time = time.time()

        # Image data extraction timing
        imgdata_start_time = time.time()
        imgdata = self.getImgData(src)
        imgdata_end_time = time.time()
        imgdata_total_time = imgdata_end_time - imgdata_start_time

        # Context extraction timing
        context = [None, None]
        context_start_time = time.time()
        if self.options["withContext"]:
            context = self.getContext(self.getImg(src))
        context_end_time = time.time()
        context_total_time = context_end_time - context_start_time
        beforeContext = context[0]
        afterContext = context[1]

        # Description generation timing
        genDesc_start_time = time.time()
        desc = self.genDesc(imgdata, src, context)
        genDesc_end_time = time.time()
        genDesc_total_time = genDesc_end_time - genDesc_start_time

        # OCR processing timing
        ocr_start_time = time.time()
        chars = ""
        if self.ocrEngine is not None:
            chars = self.genChars(imgdata, src).strip()
        ocr_end_time = time.time()
        ocr_total_time = ocr_end_time - ocr_start_time

        # Refinement processing timing
        refine_start_time = time.time()
        if self.langEngine is None:
            raise Exception("To use version 2, you must have a langEngine set.")
        refined_desc = self.langEngine.refineAlt(desc, chars, context, None)
        refine_end_time = time.time()
        refine_total_time = refine_end_time - refine_start_time

        # End total timing
        total_end_time = time.time()
        total_overall_time = total_end_time - total_start_time

        #Record dictionary to store all the timing data
        record = {
            "Image Data Extraction Time": imgdata_total_time,
            "Context Extraction Time": context_total_time,
            "Description Generation Time": genDesc_total_time,
            "OCR Processing Time": ocr_total_time,
            "Refinement Processing Time": refine_total_time,
            "Total Overall Time": total_overall_time
        }
        # Add record to benchmark_records for later CSV generation
        self.benchmark_records.append(record)

        return refined_desc

    #CSV generation
    def generate_csv(benchmark_records, csv_file_path):
        if not benchmark_records:
            print("No benchmark data available.")
            return

        # Determine the CSV field names from the keys of the first record
        fieldnames = benchmark_records[0].keys()

        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in benchmark_records:
                writer.writerow(record)
        print(f"CSV file has been generated at: {csv_file_path}")