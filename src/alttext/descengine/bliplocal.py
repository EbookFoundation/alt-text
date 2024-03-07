import os
import shutil
import subprocess
import uuid

from .descengine import DescEngine

class BlipLocal(DescEngine):
    def __init__(self, path: str) -> None:
        self.__setPath(path)
        return None

    def __setPath(self, path: str) -> str:
        self.path = path
        return self.path

    def genDesc(self, imgData: bytes, src: str, context: str = None) -> str:
        folderName = uuid.uuid4()
        ext = src.split(".")[-1]
        os.makedirs(f"{self.path}/{folderName}")
        open(f"{self.path}/{folderName}/image.{ext}", "wb+").write(imgData)
        subprocess.call(
            f"py inference.py -i ./{folderName} --batch 1 --gpu 0",
            cwd=f"{self.path}",
        )
        desc = open(f"{self.path}/{folderName}/0_captions.txt", "r").read()
        shutil.rmtree(f"{self.path}/{folderName}")
        desc = desc.split(",")
        return desc[1]