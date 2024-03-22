# Used to chunk the empty_alt_text.txt into multiple different more digestable .txt files
# Will potentially eventually be used to upload from the file right into a database of books
# Then will update the file paths, download & install the books with images

import os

input_file = "./empty_alt_text_sample.txt"  # The file path of whatever initial .txt you are working with
output_folder = "./book_outputs"


def createIndividualBookFiles(input_file, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Keep track of the last book number processed
    last_book_number = None

    with open(input_file, "r") as file:
        for line in file:
            book_number = line.split()[0]  # Extracting book number
            # Check if this line is for a new book
            if book_number != last_book_number:
                output_file_name = f"ebook_{book_number}.txt"
                output_path = os.path.join(output_folder, output_file_name)
                # print(f"Creating/Updating file for book {book_number}")
                last_book_number = book_number

            # Append to the file (creates a new file if it doesn't exist)
            with open(output_path, "a") as output_file:
                output_file.write(line)


createIndividualBookFiles(input_file, output_folder)
