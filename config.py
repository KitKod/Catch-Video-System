import os
from dotenv import load_dotenv


class Config:
    load_dotenv()
    CAMERA_TYPE = int(os.getenv("CAMERA_TYPE"))
    DEVICE_ID = int(os.getenv("DEVICE_ID"))
    FLIP = int(os.getenv("FLIP"))
    WIDTH = int(os.getenv("WIDTH"))    
    HEIGHT = int(os.getenv("HEIGHT"))
    FPS = int(os.getenv("FPS"))
