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


REPLICATE_MODELS = {
    "blip": "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
    "clip_prefix_caption": "rmokady/clip_prefix_caption:9a34a6339872a03f45236f114321fb51fc7aa8269d38ae0ce5334969981e4cd8",
    "clip-caption-reward": "j-min/clip-caption-reward:de37751f75135f7ebbe62548e27d6740d5155dfefdf6447db35c9865253d7e06",
    "img2prompt": "methexis-inc/img2prompt:50adaf2d3ad20a6f911a8a9e3ccf777b263b8596fbd2c8fc26e8888f8a0edbb5",
    "minigpt4": "daanelson/minigpt-4:b96a2f33cc8e4b0aa23eacfce731b9c41a7d9466d9ed4e167375587b54db9423",
    "image-captioning-with-visual-attention": "nohamoamary/image-captioning-with-visual-attention:9bb60a6baa58801aa7cd4c4fafc95fcf1531bf59b84962aff5a718f4d1f58986",
}


### IMPLEMENTATIONS
class ReplicateAPI(DescEngine):
    def __init__(self, key: str, model: str = "blip") -> None:
        self.__setKey(key)
        self.__setModel(model)
        return None

    def __getModel(self) -> str:
        return self.model

    def __setModel(self, modelName: str) -> str:
        if modelName not in REPLICATE_MODELS:
            raise Exception(
                f"{modelName} is not a valid model. Please choose from {list(REPLICATE_MODELS.keys())}"
            )
        self.model = REPLICATE_MODELS[modelName]
        return self.model

    def __getKey(self) -> str:
        return self.key

    def __setKey(self, key: str) -> str:
        self.key = key
        os.environ["REPLICATE_API_TOKEN"] = key
        return self.key

    def genDesc(self, imgData: bytes, src: str, context: str = None) -> str:
        base64_utf8_str = base64.b64encode(imgData).decode("utf-8")
        model = self.__getModel()
        ext = src.split(".")[-1]
        prompt = "Create alternative-text for this image."
        if context != None:
            prompt = f"Create alternative-text for this image given the following context...\n{context}"

        dataurl = f"data:image/{ext};base64,{base64_utf8_str}"
        output = replicate.run(model, input={"image": dataurl, "prompt": prompt})
        return output


class GoogleVertexAPI(DescEngine):
    def __init__(self, project_id: str, location: str, gac_path: str) -> None:
        self.project_id = project_id
        self.location = location
        vertexai.init(project=self.project_id, location=self.location)

        self.gac_path = gac_path
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
