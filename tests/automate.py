
import os
from pathlib import Path
from alttext import genAltTextV2
from descengine import genDesc
from ocrengine import genChars
from langengine import refineDesc, refineOCR #need to implement these

def read_paths_from_file(file_path):
    """Reads image paths from a given file and returns a list of tuples containing book number and path."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    paths = [line.strip().split('\t') for line in lines]
    return paths

def generate_alt_text_for_images(image_paths):
    """
    Generates alt-text for a list of image paths. Each path is a tuple containing the book number and the image path.
    """
    alt_texts = []
    for path_info in image_paths:
        book_num, image_path = path_info.split('\t')
        full_image_path = f"cache/epub/{book_num}/images/{image_path}"

        # Generate alt-text using the genAltTextV2 method
        alt_text = alt_text.genAltTextV2(full_image_path) #I don't think I am doing this right

        alt_texts.append((book_num, image_path, alt_text))

    return alt_texts

def main():
    input_file = '../empty_alt_text_sample.text' # Update this path
    output_file = '../generated_alt_texts.txt' # Update this path

    image_paths = read_paths_from_file(input_file)
    alt_texts = generate_alt_text_for_images(image_paths)

    with open(output_file, 'w') as file:
        for alt_text in alt_texts:
            file.write(f'{alt_text}\n')

if __name__ == '__main__':
    main()
