# automate.py - tests the generation of images and benchmarks the systems
# run getbooks.py then downloadbooks.py with input (.txt file), use output for next steps

# imports
import os
import sys
import time
import csv
import bs4
from bs4 import BeautifulSoup
import importlib
sys.path.append("c:/Users/ketha/Code/Senior D") #This will need to be changed system to system
AltTextHTML = importlib.import_module("alt-text.src.alttext.alttext").AltTextHTML
PrivateGPT = importlib.import_module("alt-text.src.alttext.langengine.langengine").PrivateGPT
descengine_path = 'c:/Users/ketha/Code/Senior D/alt-text/src/alttext/descengine/descengine.py'




# access downloaded books and go thru all of them
# 1. parse html file to find img src to get the before and after context (using get context funct)
# 2. generate alt text using genAltTextV2 (add benchmarking at some point)
# 3. save alt text and benchmarking in a csv (see csv file headings)

# iterate thru downloaded_books folder, pass html into parseFile



class AltTextGenerator(AltTextHTML):
    # uses the class from alttext.py
    # adds relevant benchmarking and saving methods

    def __init__(self, api_key, descengine):
        super().__init__(descengine)
        self.benchmark_records = []
        self.api_key = api_key
    #Use genAltTextV2
    #ADD benchmark time stamps
    def genAltTextV2(self, src: str, book_id, image_path, book_path) -> str:
        # Start total timing
        total_start_time = time.time()

        with open('example.txt', 'w', encoding="utf-8") as file:
            #contents = file.read()
            file.write(str(src))


        # Image data extraction timing
        imgdata_start_time = time.time()
        print("starting imaging")
        time.sleep(3)
        imgdata = self.getImgData(src)
        imgdata_end_time = time.time()
        imgdata_total_time = imgdata_end_time - imgdata_start_time

        # Context extraction timing
        context = [None, None]
        print("starting contexting")
        time.sleep(3)
        context_start_time = time.time()
        if self.options["withContext"]:
            context = self.getContext(self.getImg(src))
        context_end_time = time.time()
        context_total_time = context_end_time - context_start_time
        beforeContext = context[0]
        afterContext = context[1]

        # Description generation timing
        genDesc_start_time = time.time()
        print("starting desc")
        time.sleep(3)
        desc = self.genDesc(imgdata, src, context)
        genDesc_end_time = time.time()
        genDesc_total_time = genDesc_end_time - genDesc_start_time

        # OCR processing timing
        ocr_start_time = time.time()
        print("starting ocr")
        time.sleep(3)
        chars = ""
        if self.ocrEngine is not None:
            chars = self.genChars(imgdata, src).strip()
        ocr_end_time = time.time()
        ocr_total_time = ocr_end_time - ocr_start_time

        # Refinement processing timing
        refine_start_time = time.time()
        print("starting refinement")
        time.sleep(3)
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
            "Book": book_id,
            "Image": image_path,
            "Path": book_path,
            "Status": True, #Set false if failed, set true is worked
            "Before Context": beforeContext,
            "After Context": afterContext,
            "genDesc": desc,
            "genDesc-Start": genDesc_start_time,
            "genDesc-End": genDesc_end_time,
            "genDesc-Time": genDesc_total_time,
            "genOCR": chars,
            "genOCR-Start": ocr_start_time,
            "genOCR-End": ocr_end_time,
            "genOCR-Time": ocr_total_time,
            "refineDesc": refined_desc,
            "refineDesc-Time": refine_total_time,
            "Total Time": total_overall_time
        }
        # Add record to benchmark_records for later CSV generation
        self.benchmark_records.append(record)

        return refined_desc

    #CSV generation
    def generate_csv(self, csv_file_path, benchmark_records):
        if not benchmark_records:
            benchmark_records = self.benchmark_records

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

def import_descengine():
    #Key Stuff
    spec = importlib.util.spec_from_file_location("descengine", descengine_path)
    descengine = importlib.util.module_from_spec(spec)
    sys.modules["descengine"] = descengine
    spec.loader.exec_module(descengine)
    return descengine

def automate_process(extr_folder : str):
    # Iterate through all images in a folder to produce a table (csv) with benchmarking
    descengine = import_descengine()
    minigpt4_key = descengine.REPLICATE_MODELS['minigpt4']

    generator = AltTextGenerator(minigpt4_key, descengine)

    # Iterate thru each book in folder (ex. downloaded_books)
    if os.path.exists(extr_folder):
        for book_id in os.listdir(extr_folder):
            book_path = os.path.join(extr_folder, book_id)
            #alt-text/tests/downloaded_books\120
            if os.path.isdir(book_path):
                for filename in os.listdir(book_path):
                    filepath = os.path.join(book_path, filename)

                    # Check if the file is an HTML file
                    if filepath.endswith(".html"):

                        #extra layer should: add an extra layer to iterate through the images tab,
                        #find that image within the .html
                        #Go to alt-text generation where it will...
                        #get the context
                        #generate the alt-text for that image based on the context and other factors

                        # Use the parseFile method to parse the HTML file for the genAltText function
                        soup = generator.parseFile(filepath)
                        generator.genAltTextV2(soup, book_id, filepath, book_path)


    generator.generate_csv('test_benchmark.csv', generator.benchmark_records)

if __name__ == "__main__":
    print("Running automate.py")

    automate_process('alt-text/tests/downloaded_books')