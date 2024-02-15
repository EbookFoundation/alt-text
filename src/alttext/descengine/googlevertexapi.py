import os
import vertexai
from vertexai.vision_models import ImageTextModel, Image

from .descengine import DescEngine

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