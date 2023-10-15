from abc import ABC, abstractmethod
import typing
import bs4

class AltText(ABC):
    @abstractmethod
    def checkData(self):
        pass
    @abstractmethod
    def parse(self, html:str):
        pass
    @abstractmethod
    def parseFile(self, filename:str):
        pass
    @abstractmethod
    def getAllImgs(self):
        pass
    @abstractmethod
    def getNoAltImgs(self):
        pass
    @abstractmethod
    def setAlt(self, src:str, text:str):
        pass
    @abstractmethod
    def export(self):
        pass
    @abstractmethod
    def exportToFile(self, path:str):
        pass

class AltTextHTML(AltText):
    def __init__(self):
        return None

    def checkData(self):
        if not hasattr(self, "data"):
            raise Exception("no data set. please use .parse or .parseFile")
        return True

    def parse(self, html:str) -> bs4.BeautifulSoup:
        soup = bs4.BeautifulSoup(html, "html.parser")
        self.data = soup
        return soup
    
    def parseFile(self, filename:str) -> bs4.BeautifulSoup:
        with open(filename, encoding="utf8") as html:
            return self.parse(html)
        
    def getAllImgs(self) -> typing.List[bs4.element.Tag]:
        self.checkData()
        imgs = self.data.find_all("img")
        return imgs
    
    def getNoAltImgs(self) -> typing.List[bs4.element.Tag]:
        self.checkData()
        imgs = self.getAllImgs()
        noalt = []
        for img in imgs:
            if not "alt" in img.attrs.keys() or img.attrs["alt"].strip() == "":
                noalt.append(img)
        return noalt
    
    def setAlt(self, src:str, text:str) -> bs4.element.Tag:
        self.checkData()
        img = self.data.find("img", src=src)
        img.attrs["src"] = text
        return img
    
    def export(self) -> str:
        self.checkData()
        html = self.data.prettify()
        return html
    
    def exportToFile(self, path: str) -> str:
        html = self.export()
        with open(path, 'w', encoding='utf-8') as file:
            file.write(html)
        return path
        
if __name__ == "__main__":
    ## MAIN TEST
    print("TESTING index.py")
    alt:AltTextHTML = AltTextHTML()

    ## PARSE TEST
    html = '<html><head><title>Test</title></head><body><img src="test"/><h1>Parse me!</h1><img src="test2"/></body></html>'
    alt.parse(html)

    ## PARSEFILE TEST
    path1 = "./books/pg71856-h/pg71856-images.html"
    path2 = "./books/pg71859-h/pg71859-images.html"
    alt.parseFile(path1)

    ## GETALLIMGS & SETALT TEST
    imgs = alt.getNoAltImgs()
    print(imgs)

    
# FORMATS = ["html", "epub3"]
# format = format.lower()
# if not format in FORMATS:
#     raise Exception("{type} is not a valid type.".format(type = format))
# self.format = format
# match format:
#     case "html":
#         self.parse = self._parseHTML
#         self.parseFile = self._parseFileHTML
#         self.getAllImgs = self._getAllImgsHTML
#     case "epub3":
#         raise Exception("IMPLEMENT ME: epub3 is not supported yet")
# return None

