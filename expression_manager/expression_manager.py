import os
import displayio
import adafruit_imageload
from .expression import Expression

class ExpressionManager:
    def __init__(self, asset_dir="assets"):
        self._asset_dir = asset_dir
        self._expressions = {}
        
        bitmap, palette = adafruit_imageload.load(
                                            self._asset_dir + "/base.bmp", 
                                            bitmap=displayio.Bitmap, 
                                            palette=displayio.Palette)
        self._baseImg = displayio.TileGrid(bitmap, pixel_shader=palette)
        self._height = bitmap.height

        self.load_expressions()

    def load_expressions(self):
        expression_list = os.listdir(self._asset_dir)
        expression_list.sort()
        for expression in expression_list:
            if "." not in expression:
                self._expressions[expression] = Expression(expression, self._asset_dir)

    def get_expression_io(self, name:str, eye_index:int, mouth_index:int) -> displayio.Group:
        print("name:" + name + "  eye_index:" + str(eye_index) + "  mouth_index:" + str(mouth_index))
        expression = self._expressions[name].display(eye_index, mouth_index)

        print("!!!" + self._expressions[name]._name)

        if (eye_index > self._expressions[name].eyes_num):
            IndexError("eye index out of range")
        if (mouth_index > self._expressions[name].mouths_num):
            IndexError("mouth index out of range")

        return expression
    
    def get_expression_info(self, name:str) -> dict:
        info_dict = {}
        info_dict["name"] = name
        info_dict["eyes_num"] = self._expressions[name].eyes_num
        info_dict["mouths_num"] = self._expressions[name].mouths_num
        return info_dict
    
    def has(self, name:str) -> True|False:
        return name in self._expressions.keys()