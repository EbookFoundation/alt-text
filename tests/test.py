import sys
sys.path.append("../")
import src.alttext_FEF.alttext as alttext

if __name__ == "__main__":
    ## MAIN TEST
    print("TESTING index.py")
    alt:alttext.AltTextHTML = alttext.AltTextHTML()

    ## PARSE TEST
    html = '<html><head><title>Test</title></head><body><img src="test"/><h1>Parse me!</h1><img src="test2"/></body></html>'
    alt.parse(html)

    ## PARSEFILE TEST
    path1 = "../books/pg71856-h/pg71856-images.html"
    path2 = "../books/pg71859-h/pg71859-images.html"
    alt.parseFile(path1)

    ## GETALLIMGS & SETALT TEST
    imgs = alt.getNoAltImgs()
    print(imgs)