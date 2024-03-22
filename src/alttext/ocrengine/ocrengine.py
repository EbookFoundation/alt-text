from abc import ABC, abstractmethod


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
