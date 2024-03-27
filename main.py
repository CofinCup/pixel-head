import random
import time
import displayio
import adafruit_imageload
from adafruit_matrixportal.matrix import Matrix
from board import A4, SCL, SDA

from sensors import AudioSensor, MotionSensor, BleSensor
from controller import Controller
from expression_manager import ExpressionManager

# SET UP
_matrix = Matrix(bit_depth=6)
_display = _matrix.display
# Initialize sensors
_audio_sensor = AudioSensor(A4)
_motion_sensor = MotionSensor()
_ble_sensor = BleSensor()
_expression_manager = ExpressionManager()

_controller = Controller(_audio_sensor, _motion_sensor, _ble_sensor, _expression_manager, _display)

while(True):
    _controller.loop_once()
    # dx, dy, dz = _motion_sensor.get_direction_angle()
    # print("x: "+str(int(dx/10)*10), "  y: "+str(int(dy/10)*10)+"  z:"+str(int(dz/10)*10))
    # print(_motion_sensor.get_direction())
    # print(str(_audio_sensor.get_speaking_level()))
    # time.sleep(1)
