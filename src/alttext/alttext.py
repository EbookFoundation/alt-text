from abc import ABC, abstractmethod
import typing
import warnings
import bs4
import ebooklib
from ebooklib import epub

class AltText(ABC):
    # PARSING METHODS
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

def getSoup(content : str) -> bs4.BeautifulSoup:
    try:
        return bs4.BeautifulSoup(content, "html.parser")
    except Exception as htmlErr:
        try:
            return bs4.BeautifulSoup(content, features="xml")
        except Exception as xmlErr:
            raise Exception(f"Failed to parse the document as HTML: {htmlErr}\nFailed to parse the document as XML: {xmlErr}")


class AltTextHTML(AltText):
    def __init__(self) -> None:
        return None

    def checkData(self) -> bool:
        if not hasattr(self, "data"):
            raise Exception("no data set. please use .parse or .parseFile")
        return True

    def parse(self, html:str) -> bs4.BeautifulSoup:
        soup = getSoup(html, "html.parser")
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

class AltTextEPUB(AltText):
    def __init__(self) -> None:
        return None
    
    def checkData(self) -> bool:
        if not hasattr(self, "data"):
            raise Exception("no data set. please use .parse or .parseFile")
        return True

    def parse(self, html:str):
        raise Exception("parse: IMPLEMENT ME")

    def parseFile(self, filename:str) -> epub.EpubBook:
        book = epub.read_epub(filename, {"ignore_ncx": True})
        self.data = book
        return book

    def getAllImgs(self) -> typing.List[bs4.element.Tag]:
        documents = self.data.get_items_of_type(ebooklib.ITEM_DOCUMENT)
        imgs = []
        for docs in documents:
            # features="xml"
            soup = getSoup(docs.get_content())
            imgsInDoc = soup.find_all("img")
            for img in imgsInDoc:
                imgs.append(img)
        return imgs

    def getNoAltImgs(self) -> typing.List[bs4.element.Tag]:
        imgs = self.getAllImgs()
        noalt = []
        for img in imgs:
            if not "alt" in img.attrs.keys() or img.attrs["alt"].strip() == "":
                noalt.append(img)
        return noalt

    def setAlt(self, src:str, text:str):
        self.checkData()
        documents = self.data.get_items_of_type(ebooklib.ITEM_DOCUMENT)
        for doc in documents:
            soup = getSoup(doc.get_content())
            imgsInDoc = soup.find_all("img")
            for img in imgsInDoc:
                if img.attrs["src"] == src:
                    img.attrs["alt"] = text
                    newHtml = soup.prettify()
                    doc.set_content(newHtml.encode('utf-8'))
                    return
        raise Exception("unable to find image with src '{src}'".format(src=src))

    def export(self):
        self.checkData()
        return self.data

    def exportToFile(self, path:str) -> str:
        epub.write_epub(path, self.export())
        return path