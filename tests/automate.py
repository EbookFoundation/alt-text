# automate.py - tests the generation of images and benchmarks the systems
# run getbooks.py then downloadbooks.py with input (.txt file), use output for next steps

import os
import sys
import time
import csv

import keys

sys.path.append("../")
from src.alttext.alttext import AltTextHTML
from src.alttext.descengine.replicateapi import ReplicateAPI
from src.alttext.ocrengine.tesseract import Tesseract
from src.alttext.langengine.openaiapi import OpenAIAPI


class AltTextGenerator(AltTextHTML):
    # Use genAltTextV2
    # ADD benchmark time stamps
    def genAltTextV2(self, src: str, book_id, image_path, book_path) -> str:
        print(f"PROCESSING BOOK {book_id} | IMAGE {image_path}")
        status = False
        # Start total timing
        total_start_time = time.time()

        imgdata = self.getImgData(src)
        context = self.getContext(self.getImg(src))

        # Description generation timing
        # print("starting desc")
        genDesc_start_time = time.time()
        desc = self.genDesc(imgdata, src, context)
        genDesc_end_time = time.time()
        genDesc_total_time = genDesc_end_time - genDesc_start_time

        # OCR processing timing
        # print("starting ocr")
        ocr_start_time = time.time()
        chars = self.genChars(imgdata, src).strip()
        ocr_end_time = time.time()
        ocr_total_time = ocr_end_time - ocr_start_time

        # Refinement processing timing
        # print("starting refinement")
        refine_start_time = time.time()
        refined_desc = self.langEngine.refineAlt(desc, chars, context, None)
        refine_end_time = time.time()
        refine_total_time = refine_end_time - refine_start_time

        # End total timing
        total_end_time = time.time()
        total_overall_time = total_end_time - total_start_time

        # Record dictionary to store all the timing data
        record = {
            "book": book_id,
            "image": image_path,
            "path": book_path,
            "status": status,  # Set false if failed, set true is worked
            "beforeContext": context[0],
            "afterContext": context[1],
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
            "totalTime": total_overall_time,
        }

        print(f"FINISHED BOOK {book_id} | IMAGE {image_path}")

        return record


def generateCSV(csv_file_path: str, benchmark_records: list[dict]):
    fieldnames = benchmark_records[0].keys()

    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in benchmark_records:
            writer.writerow(record)

    print(f"CSV file has been generated at: {csv_file_path}")
    return


def benchmarkBooks(booksDir: str, srcsDir: str):
    generator = AltTextGenerator(
        ReplicateAPI(keys.ReplicateEricKey()),
        Tesseract(),
        OpenAIAPI(keys.OpenAIKey(), "gpt-3.5-turbo"),
    )

    records = []
    for bookId in os.listdir(booksDir):
        try:
            bookPath = os.path.join(booksDir, bookId)

            htmlpath = None
            for object in os.listdir(bookPath):
                if object.endswith(".html"):
                    htmlpath = os.path.join(bookPath, object)
                    break
            generator.parseFile(htmlpath)

            srcs = []
            with open(f"{srcsDir}/ebook_{bookId}.txt", "r") as file:
                for line in file:
                    srcs.append(line.split(f"{bookId}/")[1].strip())

            for src in srcs:
                try:
                    record = generator.genAltTextV2(src, bookId, src, bookPath)
                    records.append(record)
                except Exception as e:
                    print(f"Error processing image {src} in book {bookId}: {e}")
        except Exception as e:
            print(f"Error processing book {bookId}: {e}")

    generateCSV("test_benchmark.csv", records)


if __name__ == "__main__":
    print("RUNNING AUTOMATE.PY")
    benchmarkBooks("./downloaded_books", "./book_outputs")
