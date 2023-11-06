from abc import ABC, abstractmethod
import typing
from threading import Thread

import bs4
import ebooklib
from ebooklib import epub

from .ocrengine import OCREngine
from .descengine import DescEngine


### ALTTEXT CLASSES
class AltText(ABC):
    # PARSING METHODS
    @abstractmethod
    def checkData(self) -> bool:
        pass

    @abstractmethod
    def parse(self, html: str) -> bs4.BeautifulSoup | epub.EpubBook:
        pass

    @abstractmethod
    def parseFile(self, filepath: str) -> bs4.BeautifulSoup | epub.EpubBook:
        pass

    @abstractmethod
    def getAllImgs(self) -> typing.List[bs4.element.Tag]:
        pass

    @abstractmethod
    def getNoAltImgs(self) -> typing.List[bs4.element.Tag]:
        pass

    @abstractmethod
    def getImg(self, src: str) -> bs4.element.Tag:
        pass

    @abstractmethod
    def setAlt(self, src: str, text: str) -> bs4.element.Tag:
        pass

    @abstractmethod
    def setAlts(self, associations: list[dict]) -> list[bs4.element.Tag]:
        pass

    @abstractmethod
    def export(self) -> str | epub.EpubBook:
        pass

    @abstractmethod
    def exportToFile(self, path: str) -> str:
        pass

    # GENERATIVE METHODS
    @abstractmethod
    def getImgData(self, src: str) -> bytes:
        pass

    @abstractmethod
    def getContext(self, tag: bs4.Tag) -> str:
        pass

    @abstractmethod
    def genChars(self, imgData: bytes, src: str) -> str:
        pass

    @abstractmethod
    def genDesc(self, imgData: bytes, src: str, context: str = None) -> str:
        pass

    @abstractmethod
    def genAltText(
        self, src: str, withcontext: bool = False, withocr: bool = False
    ) -> str:
        pass

    @abstractmethod
    def genAssociation(
        self,
        tag: bs4.element.Tag,
        withcontext: bool = False,
        withocr: bool = False,
        withhash: bool = False,
    ) -> dict:
        pass

    @abstractmethod
    def _genAltAssociationsST(
        self,
        tags: list[bs4.element.Tag],
        withcontext: bool = False,
        withocr: bool = False,
        withhash: bool = False,
    ) -> list[dict]:
        pass

    @abstractmethod
    def _genAltAssociationsMT(
        self,
        tags: list[bs4.element.Tag],
        withcontext: bool = False,
        withocr: bool = False,
        withhash: bool = False,
    ) -> list[dict]:
        pass

    @abstractmethod
    def genAltAssociations(
        self,
        tags: list[bs4.element.Tag],
        withcontext: bool = False,
        withocr: bool = False,
        withhash: bool = False,
        multithreaded: bool = True,
    ) -> list[dict]:
        pass


### HELPER METHODS
def getSoup(content: str) -> bs4.BeautifulSoup:
    try:
        return bs4.BeautifulSoup(content, "html.parser")
    except Exception as htmlErr:
        try:
            return bs4.BeautifulSoup(content, features="xml")
        except Exception as xmlErr:
            raise Exception(
                f"Failed to parse the document as HTML: {htmlErr}\nFailed to parse the document as XML: {xmlErr}"
            )


### IMPLEMENTATIONS
class AltTextHTML(AltText):
    def __init__(
        self, descEngine: DescEngine = None, ocrEngine: OCREngine = None
    ) -> None:
        self.data = None
        self.filename = None
        self.filedir = None
        self.descEngine = descEngine
        self.ocrEngine = ocrEngine
        return None

    def checkData(self) -> bool:
        if not hasattr(self, "data") or self.data == None:
            raise Exception("no data set. please use .parse or .parseFile")
        return True

    # PARSING METHODS
    def parse(self, html: str) -> bs4.BeautifulSoup:
        soup = getSoup(html)
        self.data = soup
        return soup

    def parseFile(self, filepath: str) -> bs4.BeautifulSoup:
        with open(filepath, encoding="utf8") as html:
            l = filepath.split("/")
            self.filename = l.pop()
            self.filedir = "/".join(l) + "/"
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

    def getImg(self, src: str) -> bs4.element.Tag:
        self.checkData()
        img = self.data.find("img", src=src)
        return img

    def setAlt(self, src: str, text: str) -> bs4.element.Tag:
        self.checkData()
        img = self.data.find("img", src=src)
        img.attrs["alt"] = text
        return img

    def setAlts(self, associations: list[dict]) -> list[bs4.element.Tag]:
        self.checkData()
        tags = []
        for association in associations:
            tags.append(self.setAlt(association["src"], association["alt"]))
        return tags

    def export(self) -> str:
        self.checkData()
        html = self.data.prettify()
        return html

    def exportToFile(self, path: str) -> str:
        html = self.export()
        with open(path, "w", encoding="utf-8") as file:
            file.write(html)
        return path

    # GENERATIVE METHODS
    def __getImgFilePath(self, src: str) -> str:
        self.checkData()
        path = f"{self.filedir}{src}"
        return path

    def getImgData(self, src: str) -> bytes:
        path = self.__getImgFilePath(src)
        with open(path, "rb") as bin:
            bin = bin.read()
            return bin

    def getContext(self, tag: bs4.Tag) -> str:
        raise Exception("IMPLEMENT ME")

    def genChars(self, imgData: bytes, src: str) -> str:
        text = self.ocrEngine.genChars(imgData, src)
        return text

    def genDesc(self, imgData: bytes, src: str, context: str = None) -> str:
        alt = self.descEngine.genDesc(imgData, src, context)
        return alt

    def genAltText(
        self, src: str, withcontext: bool = False, withocr: bool = False
    ) -> str:
        imgdata = self.getImgData(src)
        context = None
        if withcontext:
            context = self.getContext(self.getImg(src))
        desc = self.genDesc(imgdata, src, context)
        alt = f"AUTO-GENERATED ALT-TEXT: {desc}"
        if withocr:
            chars = self.genChars(imgdata, src, context)
            alt = f"{alt}\nTEXT FOUND IN IMAGE: {chars}"
        return alt

    def genAssociation(
        self,
        tag: bs4.element.Tag,
        withcontext: bool = False,
        withocr: bool = False,
        withhash: bool = False,
    ) -> dict:
        src = tag.attrs["src"]
        alt = self.genAltText(src, withcontext, withocr)
        association = {"src": src, "alt": alt}
        if withhash:
            data = self.getImgData(src)
            association["hash"] = hash(data)
        return association

    def _genAltAssociationsST(
        self,
        tags: list[bs4.element.Tag],
        withcontext: bool = False,
        withocr: bool = False,
        withhash: bool = False,
    ) -> list[dict]:
        associations = []
        for tag in tags:
            associations.append(
                self.genAssociation(tag, withcontext, withocr, withhash)
            )
        return associations

    def _genAltAssociationsMT(
        self,
        tags: list[bs4.element.Tag],
        withcontext: bool = False,
        withocr: bool = False,
        withhash: bool = False,
    ) -> list[dict]:
        associations = []

        def genAppend(tag, withcontext, withocr, withhash):
            associations.append(
                self.genAssociation(
                    tag,
                    withcontext,
                    withocr,
                    withhash,
                )
            )

        threads: list[Thread] = []
        for tag in tags:
            thread = Thread(
                target=genAppend,
                args=(
                    tag,
                    withcontext,
                    withocr,
                    withhash,
                ),
            )
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        return associations

    def genAltAssociations(
        self,
        tags: list[bs4.element.Tag],
        withcontext: bool = False,
        withocr: bool = False,
        withhash: bool = False,
        multithreaded: bool = True,
    ) -> list[dict]:
        if multithreaded:
            return self._genAltAssociationsMT(tags, withcontext, withocr, withhash)
        return self._genAltAssociationsST(tags, withcontext, withocr, withhash)


class AltTextEPUB(AltText):
    def __init__(self) -> None:
        return None

    def checkData(self) -> bool:
        if not hasattr(self, "data"):
            raise Exception("no data set. please use .parse or .parseFile")
        return True

    def parse(self, epub: epub.EpubBook) -> epub.EpubBook:
        self.data = epub
        return self.data

    def parseFile(self, filepath: str) -> epub.EpubBook:
        book = epub.read_epub(filepath, {"ignore_ncx": True})
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

    def setAlt(self, src: str, text: str):
        self.checkData()
        documents = self.data.get_items_of_type(ebooklib.ITEM_DOCUMENT)
        for doc in documents:
            soup = getSoup(doc.get_content())
            imgsInDoc = soup.find_all("img")
            for img in imgsInDoc:
                if img.attrs["src"] == src:
                    img.attrs["alt"] = text
                    newHtml = soup.prettify()
                    doc.set_content(newHtml.encode("utf-8"))
                    return
        raise Exception("unable to find image with src '{src}'".format(src=src))

    def export(self) -> epub.EpubBook:
        self.checkData()
        return self.data

    def exportToFile(self, path: str) -> str:
        epub.write_epub(path, self.export())
        return path
