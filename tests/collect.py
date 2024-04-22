import random
import requests
import bs4
import time
import os


def extractImage(imgs: list[bs4.element.Tag]) -> list[bs4.element.Tag]:
    if len(imgs) == 0:
        return None
    index = random.randint(0, len(imgs) - 1)
    img = imgs[index]
    if img.has_attr("alt") and img.attrs["alt"].strip() != "":
        return img
    return extractImage(imgs[:index] + imgs[index + 1 :])


def collect(
    num: int, image_output: str = "images.txt", alt_output: str = "alts.txt"
) -> int:
    """
    Collect images with alt-text from random ebooks

    Args:
        num (int): Number of images to collect.
        image_output (str, optional): Path to output image URLs. Defaults to "images.txt".
        alt_output (str, optional): Path to output alt-text. Defaults to "alts.txt".
    """
    count = 0
    while count < num:
        time.sleep(0.5)
        bookid = random.randint(1, 70000)
        bookurl = f"https://gutenberg.org/cache/epub/{bookid}/pg{bookid}-images.html"

        response = requests.get(bookurl)
        if response.status_code != 200:
            print(f"Failed to fetch book {bookid}.")
            continue

        soup = bs4.BeautifulSoup(response.text, "html.parser")
        div = soup.find("div", id="pg-machine-header")
        if not div:
            print(f"No 'pg-machine-header' found in book {bookid}.")
            continue

        languageP = div.find_all(recursive=False)[3]
        if languageP.text.strip() != "Language: English":
            print(f"Book {bookid} is not in English.")
            continue

        imgs: list[bs4.element.Tag] = soup.find_all("img")
        img = extractImage(imgs)
        if img is None:
            print(
                f"Out of {len(imgs)} images, no images with alt-text found in book {bookid}."
            )
            continue

        with open(image_output, "a") as imagefile:
            imagefile.write(f"{bookid} cache/epub/{bookid}/{img['src']}\n")
        with open(alt_output, "a") as altfile:
            altfile.write(f"{img['alt'].encode('ascii', 'ignore').decode()}\n")

        count += 1

    return True


def split(input_file, book_output, image_output):
    with open(input_file, "r") as file:
        for line in file:
            book_number = line.split()[0]  # Extracting book number
            image = line.split()[1]  # Extracting image

            with open(book_output, "a") as output_file:
                output_file.write(f"{book_number}\n")
            with open(image_output, "a") as output_file:
                output_file.write(f"{image}\n")


if __name__ == "__main__":
    # collect(150)
    split("images.txt", "books.txt", "images2.txt")
