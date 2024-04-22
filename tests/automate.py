# automate.py - tests the generation of images and benchmarks the systems
# run getbooks.py then downloadbooks.py with input (.txt file), use output for next steps

import os
import sys
import time
import csv

import keys

sys.path.append("../")
from src.alttext.alttext import AltTextHTML
from src.alttext.descengine.descengine import DescEngine
from src.alttext.descengine.replicateapi import ReplicateAPI
from src.alttext.descengine.bliplocal import BlipLocal
from src.alttext.descengine.googlevertexapi import GoogleVertexAPI
from src.alttext.ocrengine.tesseract import Tesseract
from src.alttext.langengine.openaiapi import OpenAIAPI
from src.alttext.langengine.privategpt import PrivateGPT


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
        genDesc = None
        with open("./results/llava-13b.csv", mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["book"] == book_id and row["image"] == src:
                    genDesc = row["genDesc"]
                    break
        if genDesc == None:
            raise Exception("Description not found in llava-13b.csv")

        # OCR processing timing
        # print("starting ocr")
        ocr_start_time = time.time()
        chars = self.genChars(imgdata, src).strip()
        ocr_end_time = time.time()
        ocr_total_time = ocr_end_time - ocr_start_time

        # Refinement processing timing
        # print("starting refinement")
        refine_start_time = time.time()
        if context[0] is not None:
            context[0] = context[0][:1000]
        if context[1] is not None:
            context[1] = context[1][:1000]
        refined_desc = self.langEngine.refineAlt(genDesc, chars[:1000], context, None)
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
            "genDesc": genDesc,
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
        # OpenAIAPI(keys.OpenAIKey(), "gpt-4-0125-preview"),
        PrivateGPT("http://127.0.0.1:8001"),
    )

    records = []
    for bookId in os.listdir(srcsDir):
        bookId = bookId.split("_")[1].split(".")[0]
        time.sleep(1)
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
                    print(f"ERROR processing image {bookId} | {src}: {e}")
        except Exception as e:
            print(f"ERROR processing book {bookId}: {e}")

    generateCSV("private-gpt.csv", records)


def benchmarkDescEngine(
    descEngine: DescEngine, booksDir: str, srcsDir: str, outputFilename: str
):
    generator = AltTextHTML(descEngine)

    records = []
    for bookId in os.listdir(srcsDir):
        bookId = bookId.split("_")[1].split(".")[0]
        try:
            print("STARTING BOOK ID: ", bookId)
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
                time.sleep(8)
                try:
                    print("STARTING IMAGE: ", src)
                    context = generator.getContext(generator.getImg(src))
                    genDesc_start_time = time.time()
                    desc = generator.genDesc(generator.getImgData(src), src, context)
                    print(f"TEST: {desc}")
                    genDesc_end_time = time.time()
                    genDesc_total_time = genDesc_end_time - genDesc_start_time
                    record = {
                        "book": bookId,
                        "image": src,
                        "path": bookPath,
                        # "beforeContext": context[0],
                        # "afterContext": context[1],
                        "genDesc": desc.replace('"', "'"),
                        "genDesc-Start": genDesc_start_time,
                        "genDesc-End": genDesc_end_time,
                        "genDesc-Time": genDesc_total_time,
                    }
                    records.append(record)
                except Exception as e:
                    print(f"ERROR processing image {bookId} | {src}: {e}")
        except Exception as e:
            print(f"ERROR processing book {bookId}: {e}")

    generateCSV(outputFilename, records)


if __name__ == "__main__":
    print("RUNNING AUTOMATE.PY")
    benchmarkBooks("./downloaded_books", "./book_outputs")
    # benchmarkDescEngine(
    # ReplicateAPI(
    #     keys.ReplicateEricKey(), modelName="image-captioning-with-visual-attention"
    # ),
    # BlipLocal("C:/Users/dacru/Desktop/ALT/image-captioning"),
    #     GoogleVertexAPI(keys.VertexProject(), keys.VertexRegion(), keys.VertexGAC()),
    #     "./downloaded_books",
    #     "./book_outputs2",
    #     "vertexai.csv",
    # )
