import sys
sys.path.append("../")
import src.alttext.alttext as alttext
import ebooklib

HTML1 = "../books/pg71856-h/pg71856-images.html"
HTML2 = "../books/pg71859-h/pg71859-images.html"

EPUB1 = "../books/pg71856-images-3.epub"
EPUB2 = "../books/pg71908-images-3.epub"
EPUB3 = "../books/seuss.epub"

def testHTML():
    ## MAIN TEST
    print("TESTING HTML")
    altHTML:alttext.AltTextHTML = alttext.AltTextHTML()

    ## PARSE TEST
    html = '<html><head><title>Test</title></head><body><img src="test"/><h1>Parse me!</h1><img src="test2"/></body></html>'
    altHTML.parse(html)

    ## PARSEFILE TEST
    altHTML.parseFile(HTML1)

    ## GETALLIMGS & SETALT TEST
    imgs = altHTML.getNoAltImgs()
    print(imgs)

def testEPUB():
    print("TESTING EPUB")
    altEPUB:alttext.AltTextEPUB = alttext.AltTextEPUB()

    altEPUB.parseFile(EPUB2)    
    imgs = altEPUB.getNoAltImgs()
    print(imgs)
    # img = imgs[0]
    # print(img)
    # src = img.attrs["src"]
    # altEPUB.setAlt(src, "TEST ALT")
    # print(altEPUB.getAllImgs())

if __name__ == "__main__":
    # testHTML()
    testEPUB()