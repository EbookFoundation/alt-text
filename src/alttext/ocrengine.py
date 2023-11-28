from abc import ABC, abstractmethod
from PIL import Image
from io import BytesIO

import pytesseract


### OCRENGINE ABSTRACT
class OCREngine(ABC):
    @abstractmethod
    def genChars(self, imgData: bytes, src: str, context: str = None) -> str:
        """Searches for characters in an image.

        Args:
            imgData (bytes): Image data in bytes.
            src (str): Image source.
            context (str, optional): Context of an image. See getContext in alttext for more information. Defaults to None.

        Returns:
            str: Characters found in an image.
        """
        pass


### TEST CLASS
class _TOCREngine(OCREngine):
    def genChars(self, imgData: bytes, src: str, context: str = None) -> str:
        return f"TEST {src}"


### IMPLEMENTATIONS
class Tesseract(OCREngine):
    def __init__(self) -> None:
        self.customPath = None
        return None

    def _setTesseract(self, path: str) -> bool:
        self.customPath = path
        pytesseract.pytesseract.tesseract_cmd = path
        return True

    def genChars(self, imgData: bytes, src: str, context: str = None) -> str:
        image = Image.open(BytesIO(imgData))
        return pytesseract.image_to_string(image)
