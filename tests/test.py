import sys

sys.path.append("../")
import src.alttext.alttext as alttext
import src.alttext.descengine as descengine
import src.alttext.ocrengine as ocrengine
import src.alttext.langengine as langengine
import keys

# HTML BOOK FILEPATHS
HTML_BIRD = "../books/pg30221-h/pg30221-images.html"
HTML_HUNTING = "../books/pg37122-h/pg37122-images.html"
HTML_MECHANIC = "../books/pg71856-h/pg71856-images.html"
HTML_INFINITY = "../books/pg71859-h/pg71859-images.html"

# EPUB BOOK FILEPATHS
EPUB1 = "../books/pg71856-images-3.epub"
EPUB2 = "../books/pg71908-images-3.epub"
EPUB3 = "../books/seuss.epub"

HOST1 = "http://127.0.0.1:8001"


def testHTML():
    print("TESTING HTML")

    # alt: alttext.AltTextHTML = alttext.AltTextHTML(
    #     # descengine.ReplicateAPI(keys.ReplicateEricKey(), "blip"),
    #     # ocrengine.Tesseract(),
    #     # langengine.PrivateGPT(HOST1),
    # )

    # alt: alttext.AltTextHTML = alttext.AltTextHTML(
    #     descengine.BlipLocal("C:/Users/dacru/Desktop/Codebase/ALT/image-captioning"),
    #     options={"version": 1},
    # )

    alt: alttext.AltTextHTML = alttext.AltTextHTML(
        descengine.BlipLocal("C:/Users/dacru/Desktop/Codebase/ALT/image-captioning"),
        ocrengine.Tesseract(),
        langengine.PrivateGPT(HOST1),
    )

    alt.parseFile(HTML_HUNTING)
    imgs = alt.getAllImgs()
    src = imgs[4].attrs["src"]
    print(src)
    print(alt.genAltText(src))

    # desc = alt.genDesc(alt.getImgData(src), src)
    # print(desc)
    # associations = alt.genAltAssociations(imgs)
    # print(associations)


if __name__ == "__main__":
    testHTML()
