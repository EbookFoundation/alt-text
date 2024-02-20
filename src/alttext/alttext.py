from abc import ABC, abstractmethod
import typing
from threading import Thread

import bs4
import ebooklib
from ebooklib import epub

from .descengine.descengine import DescEngine
from .ocrengine.ocrengine import OCREngine
from .langengine.langengine import LangEngine


DEFOPTIONS = {
    "withContext": True,
    "withHash": True,
    "multiThreaded": True,
    "version": 2,
}


### ALTTEXT CLASSES
class AltText(ABC):
    @abstractmethod
    def setDescEngine(self, descEngine: DescEngine) -> bool:
        """Sets current description engine.

        Args:
            descEngine (DescEngine): A description engine.

        Returns:
            bool: True if successful.
        """
        pass

    @abstractmethod
    def setOCREngine(self, ocrEngine: OCREngine) -> bool:
        """Sets current OCR engine.

        Args:
            ocrEngine (OCREngine): An OCR engine.

        Returns:
            bool: True if successful.
        """
        pass

    @abstractmethod
    def setLangEngine(self, langEngine: LangEngine) -> bool:
        """Sets current language engine.

        Args:
            langEngine (LangEngine): A language engine.

        Returns:
            bool: True if successful.
        """
        pass

    @abstractmethod
    def setOptions(self, options: dict) -> bool:
        """Sets current options.

        Args:
            options (dict): A subset of DEFOPTIONS. See DEFOPTIONS constant for possible fields.

        Returns:
            bool: True if successful.
        """
        pass

    @abstractmethod
    def checkData(self) -> bool:
        """Checks if current data exists.

        Returns:
            bool: True if data exists.

        Raises:
            Exception: If no data exists.
        """
        pass

    # PARSING METHODS
    @abstractmethod
    def parse(self, data: str) -> bs4.BeautifulSoup | epub.EpubBook:
        """Parses data into a BeautifulSoup or EpubBook object.

        Args:
            data (str): HTML or EPUB data.

        Returns:
            bs4.BeautifulSoup | epub.EpubBook: The BeautifulSoup or EpubBook object stored in self.data.
        """
        pass

    @abstractmethod
    def parseFile(self, filepath: str) -> bs4.BeautifulSoup | epub.EpubBook:
        """Parses data from a file into a BeautifulSoup or EpubBook object.

        Args:
            filepath (str): Path to HTML or EPUB file.

        Returns:
            bs4.BeautifulSoup | epub.EpubBook: The BeautifulSoup or EpubBook object stored in self.data.
        """
        pass

    @abstractmethod
    def getAllImgs(self) -> typing.List[bs4.element.Tag]:
        """Gets all img tags.

        Returns:
            typing.List[bs4.element.Tag]: A list of img tags.
        """
        pass

    @abstractmethod
    def getNoAltImgs(self) -> typing.List[bs4.element.Tag]:
        """Gets all img tags that either do not have an alt attribute or alt.strip() is an empty string.

        Returns:
            typing.List[bs4.element.Tag]: A list of img tags.
        """
        pass

    @abstractmethod
    def getImg(self, src: str) -> bs4.element.Tag:
        """Gets an img tag given a src.

        Args:
            src (str): Image source.

        Returns:
            bs4.element.Tag: An img tag.
        """
        pass

    @abstractmethod
    def setAlt(self, src: str, text: str) -> bs4.element.Tag:
        """Sets the alt of an img tag given a src.

        Args:
            src (str): Image source.
            text (str): New alt-text.

        Returns:
            bs4.element.Tag: Newly modified img tag.
        """
        pass

    @abstractmethod
    def setAlts(self, associations: list[dict]) -> list[bs4.element.Tag]:
        """Sets the alt of multiple img tags given a list of associations.

        Args:
            associations (list[dict]): A list of associations. Must have keys "src" and "alt".

        Returns:
            list[bs4.element.Tag]: A list of newly modified img tags.
        """
        pass

    @abstractmethod
    def export(self) -> str | epub.EpubBook:
        """Exports the current data.

        Returns:
            str | epub.EpubBook: A string of HTML or an epub.EpubBook object.
        """
        pass

    @abstractmethod
    def exportToFile(self, path: str) -> str:
        """Exports the current data to a file.

        Args:
            path (str): A path to the file to be written.

        Returns:
            str: The path to the file written.
        """
        pass

    # GENERATIVE METHODS
    @abstractmethod
    def ingest(self) -> bool:
        """Uploads the current data and to the language engine for ingestion.
        This allows the language engine to reference the current data as a document.

        Returns:
            bool: True if successful.

        Raises:
            Exception: If no langEngine is set.
        """
        pass

    @abstractmethod
    def degest(self) -> bool:
        """Deletes the current data from the language engine.

        Returns:
            bool: True if successful.

        Raises:
            Exception: If no langEngine is set.
        """
        pass

    @abstractmethod
    def getImgData(self, src: str) -> bytes:
        """Gets byte data of an image given a src.

        Args:
            src (str): Image source.

        Returns:
            bytes: Image data as bytes.
        """
        pass

    @abstractmethod
    def getContext(self, tag: bs4.Tag) -> list[str]:
        """Gets the context of an img tag.
        Context being the text immediately before and after the img tag.

        Args:
            tag (bs4.Tag): The img tag to get context for.

        Returns:
            list[str]: A list of length 2. The first element is the text immediately before the img tag. The second element is the text immediately after the img tag.
        """
        pass

    @abstractmethod
    def genChars(self, imgData: bytes, src: str) -> str:
        """Searches for characters in an image.

        Args:
            imgData (bytes): Image data as bytes.
            src (str): Source of the image.

        Returns:
            str: String of characters found in the image.
        """
        pass

    @abstractmethod
    def genDesc(self, imgData: bytes, src: str, context: str = None) -> str:
        """Generates a description of an image.

        Args:
            imgData (bytes): Image data as bytes.
            src (str): Source of the image.
            context (str, optional): Context for an image. See getContext for more information. Defaults to None.

        Returns:
            str: Description of the image.
        """
        pass

    @abstractmethod
    def genAltTextV1(self, src: str) -> str:
        """Generates alt-text for an image given its source.
        Uses V1 Dataflow model. This means the description and characters are generated and optionally refined separately.

        Args:
            src (str): Source of the image.

        Returns:
            str: Generated alt-text for the image.
        """
        pass

    @abstractmethod
    def genAltTextV2(self, src: str) -> str:
        """Generates alt-text for an image given its source.
        Uses V2 Dataflow model. This means the description and characters are generated and then alt-text is generated using both pieces of information.

        Args:
            src (str): Source of the image.

        Returns:
            str: Generated alt-text for the image.
        """
        pass

    @abstractmethod
    def genAltText(self, src: str) -> str:
        """Generates alt-text for an image given its source and current options.

        Args:
            src (str): Source of the image.

        Returns:
            str: Generated alt-text for the image.
        """
        pass

    @abstractmethod
    def genAssociation(
        self,
        tag: bs4.element.Tag,
    ) -> dict:
        """Generates alt-text and returns an association given an img tag and current options.

        Args:
            tag (bs4.element.Tag): Image tag to make an association for.

        Returns:
            dict: The association. Must have keys "src" and "alt". If "withHash" is True, must also have key "hash".
        """
        pass

    @abstractmethod
    def _genAltAssociationsST(
        self,
        tags: list[bs4.element.Tag],
    ) -> list[dict]:
        """Generates alt-text and creates associations given a list of img tags and current options.
        Single threaded implementation.

        Args:
            tags (list[bs4.element.Tag]): List of img tags to make associations for.

        Returns:
            list[dict]: List of associations. Must have keys "src" and "alt". If "withHash" is True, must also have key "hash".
        """
        pass

    @abstractmethod
    def _genAltAssociationsMT(
        self,
        tags: list[bs4.element.Tag],
    ) -> list[dict]:
        """Generates alt-text and creates associations given a list of img tags and current options.
        Multi threaded implementation.

        Args:
            tags (list[bs4.element.Tag]): List of img tags to make associations for.

        Returns:
            list[dict]: List of associations. Must have keys "src" and "alt". If "withHash" is True, must also have key "hash".
        """
        pass

    @abstractmethod
    def genAltAssociations(
        self,
        tags: list[bs4.element.Tag],
    ) -> list[dict]:
        """Generates alt-text and creates associations given a list of img tags and current options.
        Automatically selects mutli or single threaded implementation based on current options.

        Args:
            tags (list[bs4.element.Tag]): List of img tags to make associations for.

        Returns:
            list[dict]: List of associations. Must have keys "src" and "alt". If "withHash" is True, must also have key "hash".
        """
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
        self,
        descEngine: DescEngine,
        ocrEngine: OCREngine = None,
        langEngine: LangEngine = None,
        options: dict = {},
    ) -> None:
        self.data = None
        self.filename = None
        self.filedir = None

        self.descEngine = descEngine
        self.ocrEngine = ocrEngine
        self.langEngine = langEngine

        self.options = DEFOPTIONS
        for key in dict.keys(options):
            self.options[key] = options[key]

        return None

    def setDescEngine(self, descEngine: DescEngine) -> bool:
        self.descEngine = descEngine
        return True

    def setOCREngine(self, ocrEngine: OCREngine) -> bool:
        self.descEngine = ocrEngine
        return True

    def setLangEngine(self, langEngine: LangEngine) -> bool:
        self.descEngine = langEngine
        return True

    def setOptions(self, options: dict) -> bool:
        for key in dict.keys(options):
            self.options[key] = options[key]
        return True

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
            self.filepath = filepath.replace("\\", "/")
            l = self.filepath.split("/")
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
    def ingest(self) -> bool:
        if self.langEngine == None:
            raise Exception(
                "To use ingest, you must have an appropriate langEngine set."
            )
        with open(self.filepath, "rb") as html:
            self.langEngine.ingest(self.filename, html)
        return True

    def degest(self) -> bool:
        if self.langEngine == None:
            raise Exception(
                "To use degest, you must have an appropriate langEngine set."
            )
        self.langEngine.degest(self.filename)
        return True

    def __getImgFilePath(self, src: str) -> str:
        self.checkData()
        path = f"{self.filedir}{src}"
        return path

    def getImgData(self, src: str) -> bytes:
        path = self.__getImgFilePath(src)
        with open(path, "rb") as bin:
            bin = bin.read()
            return bin

    def getContext(self, tag: bs4.Tag) -> list[str]:
        context = [None, None]
        elem = tag
        text = ""
        try:
            text = elem.text.strip()
            while text == "":
                elem = elem.previous_element
                text = elem.text.strip()
            context[0] = text
        except:
            print("error 0")
            context[0] = None
        elem = tag
        text = ""
        try:
            text = elem.text.strip()
            while text == "":
                elem = elem.next_element
                text = elem.text.strip()
            context[1] = text
        except:
            print("error 1")
            context[1] = None
        print(context)
        return context

    def genChars(self, imgData: bytes, src: str) -> str:
        text = self.ocrEngine.genChars(imgData, src)
        return text

    def genDesc(self, imgData: bytes, src: str, context: str = None) -> str:
        alt = self.descEngine.genDesc(imgData, src, context)
        return alt

    def genAltTextV1(self, src: str) -> str:
        imgdata = self.getImgData(src)
        context = None
        if self.options["withContext"]:
            context = self.getContext(self.getImg(src))
        desc = self.genDesc(imgdata, src, context)
        if self.langEngine != None:
            chars = self.langEngine.refineDesc(desc)

        alt = f"IMAGE CAPTION: {desc}"
        if self.ocrEngine != None:
            chars = self.genChars(imgdata, src)
            if self.langEngine != None:
                chars = self.langEngine.refineOCR(chars)
            alt = f"{alt}\nTEXT IN IMAGE: {chars}"

        return alt

    def genAltTextV2(self, src: str) -> str:
        imgdata = self.getImgData(src)
        context = [None, None]
        if self.options["withContext"]:
            context = self.getContext(self.getImg(src))
        desc = self.genDesc(imgdata, src, context)
        chars = ""
        if self.ocrEngine != None:
            chars = self.genChars(imgdata, src).strip()

        if self.langEngine == None:
            raise Exception("To use version 2, you must have a langEngine set.")

        return self.langEngine.refineAlt(desc, chars, context, None)

    def genAltText(self, src: str) -> str:
        if self.options["version"] == 1:
            return self.genAltTextV1(src)
        return self.genAltTextV2(src)

    def genAssociation(
        self,
        tag: bs4.element.Tag,
    ) -> dict:
        src = tag.attrs["src"]
        alt = self.genAltText(src)
        association = {"src": src, "alt": alt}
        if self.options["withHash"]:
            data = self.getImgData(src)
            association["hash"] = hash(data)
        return association

    def _genAltAssociationsST(self, tags: list[bs4.element.Tag]) -> list[dict]:
        associations = []
        for tag in tags:
            associations.append(self.genAssociation(tag))
        return associations

    def _genAltAssociationsMT(
        self,
        tags: list[bs4.element.Tag],
    ) -> list[dict]:
        associations = []

        def genAppend(tag):
            associations.append(self.genAssociation(tag))

        threads: list[Thread] = []
        for tag in tags:
            thread = Thread(
                target=genAppend,
                args=(tag,),
            )
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        return associations

    def genAltAssociations(
        self,
        tags: list[bs4.element.Tag],
    ) -> list[dict]:
        if self.options["multiThreaded"]:
            return self._genAltAssociationsMT(tags)
        return self._genAltAssociationsST(tags)


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
