# The goal of this file is to download the books and unzip them to be used by automate.py!

import os
import requests
import zipfile
import re

folder_path = "book_outputs"
download_folder = "downloaded_books/download_files"
extraction_folder = "downloaded_books"


def downloadAndUnzipBooks(folder_path, download_folder, extraction_folder):
    base_url = "https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}-h.zip"

    # Ensure the download and extraction folders exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    if not os.path.exists(extraction_folder):
        os.makedirs(extraction_folder)

    # Iterate through each text file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            # Use regex to extract only the numeric part of the book ID
            match = re.search(r"\d+", filename)
            if match:
                book_id = match.group()
                zip_file_path = os.path.join(download_folder, f"{book_id}.zip")

                # Check if the zip file already exists
                if not os.path.isfile(zip_file_path):
                    url = base_url.format(book_id=book_id)

                    # Download the zip file
                    try:
                        response = requests.get(url)
                        response.raise_for_status()  # Raise an error for bad responses

                        # Save the zip file to the specified download folder
                        with open(zip_file_path, "wb") as zip_file:
                            zip_file.write(response.content)
                        print(
                            f"Downloaded {book_id}.zip successfully to {download_folder}."
                        )
                    except requests.RequestException as e:
                        print(f"Error downloading {book_id}.zip: {e}")
                else:
                    print(f"{book_id}.zip already exists. Skipping download.")

                # Check if the book's extraction folder already exists
                book_extraction_folder = os.path.join(extraction_folder, book_id)
                if not os.path.exists(book_extraction_folder):
                    try:
                        # Unzip the file into the specified extraction folder
                        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                            zip_ref.extractall(book_extraction_folder)
                        print(f"Extracted {book_id}.zip to {book_extraction_folder}.")
                    except zipfile.BadZipFile:
                        print(
                            f"Error unzipping {book_id}.zip: The file may be corrupt or not a zip file."
                        )
                else:
                    print(
                        f"Extraction folder for {book_id} already exists. Skipping extraction."
                    )
            else:
                print(f"No book ID found in {filename}")


if __name__ == "__main__":
    downloadAndUnzipBooks(folder_path, download_folder, extraction_folder)
