from abc import ABC, abstractmethod
from PIL import Image
from io import BytesIO

import pytesseract


### OCRENGINE CLASSES
class OCREngine(ABC):
    @abstractmethod
    def genChars(self, imgData: bytes, src: str, context: str = None) -> str:
        pass


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
