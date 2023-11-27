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

    alt: alttext.AltTextHTML = alttext.AltTextHTML(
        # descengine.GoogleVertexAPI(
        #     keys.VertexProject(), keys.VertexRegion(), keys.VertexGAC()
        # ),
        # descengine.ReplicateMiniGPT4API(keys.ReplicateEricKey()),
        descengine.ReplicateClipAPI(keys.ReplicateEricKey()),
        ocrengine.Tesseract(),
        langengine.PrivateGPT(HOST1),
    )
    alt.parseFile(HTML_HUNTING)


if __name__ == "__main__":
    testHTML()
