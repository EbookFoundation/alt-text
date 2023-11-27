from abc import ABC, abstractmethod
import base64
import os

import replicate
import vertexai
from vertexai.vision_models import ImageTextModel, Image


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


### TEST CLASS
class _TDescEngine(DescEngine):
    def __init__(self):
        return None

    def genDesc(self, imgData: bytes, src: str, context: str = None) -> str:
        return f"TEST {src}"


### IMPLEMENTATIONS
class ReplicateMiniGPT4API(DescEngine):
    def __init__(self, key: str) -> None:
        self.__setKey(key)
        return None

    def __getKey(self) -> str:
        if not hasattr(self, "data") or self.key == None:
            raise Exception("no key set. please use ._setKey(key:str)")
        return self.key

    def __setKey(self, key: str) -> bool:
        self.key = key
        os.environ["REPLICATE_API_TOKEN"] = key
        return True

    def genDesc(self, imgData: bytes, src: str, context: str = None) -> str:
        base64_utf8_str = base64.b64encode(imgData).decode("utf-8")
        model = "daanelson/minigpt-4:b96a2f33cc8e4b0aa23eacfce731b9c41a7d9466d9ed4e167375587b54db9423"
        ext = src.split(".")[-1]
        prompt = "Create alternative-text for this image."
        if context != None:
            prompt = f"Create alternative-text for this image given the following context...\n{context}"

        dataurl = f"data:image/{ext};base64,{base64_utf8_str}"
        output = replicate.run(model, input={"image": dataurl, "prompt": prompt})
        return output


class ReplicateClipAPI(DescEngine):
    def __init__(self, key: str) -> None:
        self.__setKey(key)
        return None

    def __getKey(self) -> str:
        if not hasattr(self, "data") or self.key == None:
            raise Exception("no key set. please use ._setKey(key:str)")
        return self.key

    def __setKey(self, key: str) -> bool:
        self.key = key
        os.environ["REPLICATE_API_TOKEN"] = key
        return True

    def genDesc(self, imgData: bytes, src: str, context: str = None) -> str:
        base64_utf8_str = base64.b64encode(imgData).decode("utf-8")
        model = "rmokady/clip_prefix_caption:9a34a6339872a03f45236f114321fb51fc7aa8269d38ae0ce5334969981e4cd8"
        ext = src.split(".")[-1]
        dataurl = f"data:image/{ext};base64,{base64_utf8_str}"
        output = replicate.run(model, input={"image": dataurl})
        return output


class GoogleVertexAPI(DescEngine):
    def __init__(self, project_id: str, location: str, gac_path: str) -> None:
        self.project_id = project_id
        self.location = location
        self.gac_path = gac_path

        vertexai.init(project=self.project_id, location=self.location)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.gac_path
        return None

    def __setProject(self, project_id: str):
        self.project_id = project_id
        vertexai.init(project=self.project_id, location=self.location)

    def __setLocation(self, location: str):
        self.location = location
        vertexai.init(project=self.project_id, location=self.location)

    def __setGAC(self, gac_path: str):
        self.gac_path = gac_path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.gac_path

    def genDesc(self, imgData: bytes, src: str, context: str = None) -> str:
        model = ImageTextModel.from_pretrained("imagetext@001")
        source_image = Image(imgData)
        captions = model.get_captions(
            image=source_image,
            number_of_results=1,
            language="en",
        )
        return captions[0]
