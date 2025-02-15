from PIL import Image, ImageFile
import os
from constants import TEMP_IMAGE
from config import Config


def image_worker(
        path: str,
        k: float
) -> tuple[int, int]:
    img: ImageFile = Image.open(path)
    width: int = int(img.width * k)
    height: int = int(img.height * k)
    image: Image = img.resize((width, height))
    parts: list[str] = path.split('/')
    name, ext = parts[-1].split('.')
    out_name: str = name + TEMP_IMAGE + '.' + ext
    cwd: str = os.getcwd()
    Config.TERMINAL_IMAGE = f'{cwd}/{out_name}'.replace('\\', '/')
    image.save(Config.TERMINAL_IMAGE)
    img.close()
    return width, height