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
