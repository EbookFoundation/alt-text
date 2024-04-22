# Used to chunk the empty_alt_text.txt into multiple different more digestable .txt files
# Will potentially eventually be used to upload from the file right into a database of books
# Then will update the file paths, download & install the books with images

import os

input_file = "./images.txt"
output_folder = "./book_outputs"


def splitSampleByBook(input_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(input_file, "r") as file:
        for line in file:
            book_number = line.split()[0]  # Extracting book number
            output_file_name = f"ebook_{book_number}.txt"
            output_path = os.path.join(output_folder, output_file_name)

            with open(output_path, "a") as output_file:
                output_file.write(line)


if __name__ == "__main__":
    splitSampleByBook(input_file, output_folder)
