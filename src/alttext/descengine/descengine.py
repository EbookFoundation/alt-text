from abc import ABC, abstractmethod

### DESCENGINE CLASSES
class DescEngine(ABC):
    @abstractmethod
    def genDesc(self, imgData: bytes, src: str, context: str = None) -> str:
        """Generates description for an image.

        Args:
            imgData (bytes): Image data in bytes.
            src (str): Source of image.
            context (str, optional): Context of image. See getContext in alttext for more information. Defaults to None.

        Returns:
            str: _description_
        """
        pass
