import os
import displayio
import adafruit_imageload

import struct
# from PIL import Image

class Expression():
    def __init__(self, name:str, asset_dir:str):
        self._name = name
        self._asset_dir = asset_dir+"/"+name
        self._eyes, self._eyes_num = self.load_eyes()
        self._mouths, self._mouths_num = self.load_mouths()
        self._display_group = displayio.Group()
        self._display_group.append(self._eyes[0])
        self._display_group.append(self._mouths[0])
        
    @property
    def eyes_num(self):
        return self._eyes_num
    
    @property
    def mouths_num(self):
        return self._mouths_num
    
    def load_eyes(self):
        dir_list = os.listdir(self._asset_dir)
        dir_list.sort()
        eyes = []
        for file_name in dir_list:
            if file_name.startswith("eye_"):
                index = file_name.split("_")[1]
                bitmap, palette = adafruit_imageload.load(
                                    self._asset_dir + "/" + file_name, bitmap=displayio.Bitmap, 
                                    palette=displayio.Palette)
                for color_index, color in enumerate(palette):
                    if color == 0xff00ff:
                        palette.make_transparent(color_index)
                eyes.insert(len(eyes), displayio.TileGrid(bitmap, pixel_shader=palette))
        return eyes, len(eyes)

    def load_mouths(self):
        dir_list = os.listdir(self._asset_dir)
        dir_list.sort()
        mouths = []
        for file_name in dir_list:
            if file_name.startswith("mouth_"):
                index = file_name.split("_")[1]
                bitmap, palette = adafruit_imageload.load(
                                    self._asset_dir + "/" + file_name, bitmap=displayio.Bitmap, 
                                    palette=displayio.Palette)
                for color_index, color in enumerate(palette):
                    if color == 0xff00ff:
                        palette.make_transparent(color_index)
                mouths.insert(len(mouths), displayio.TileGrid(bitmap, pixel_shader=palette))
        return mouths, len(mouths)
    
    def display(self, eye_index, mouth_index):
        self._display_group.pop()
        self._display_group.pop()
        self._display_group.append(self._eyes[eye_index])
        self._display_group.append(self._mouths[mouth_index])
        return self._display_group
