import sys

sys.path.append("../")
import src.alttext.alttext as alttext
import src.alttext.descengine as descengine
import src.alttext.ocrengine as ocrengine
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


def testHTML():
    print("TESTING HTML")

    alt: alttext.AltTextHTML = alttext.AltTextHTML(
        descengine.GoogleVertexAPI(
            keys.VertexProject(), keys.VertexRegion(), keys.VertexGAC()
        ),
        ocrengine.Tesseract(),
    )
    alt.parseFile(HTML_INFINITY)

    imgs = alt.getAllImgs()
    print(imgs)
    l = alt.genAltAssociations(imgs, False, False, True, True)
    print(l)


def testEPUB():
    print("TESTING EPUB")
    altEPUB: alttext.AltTextEPUB = alttext.AltTextEPUB()

    altEPUB.parseFile(EPUB2)
    imgs = altEPUB.getNoAltImgs()
    print(imgs)


if __name__ == "__main__":
    testHTML()
    # testEPUB()
