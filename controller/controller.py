import time
import random
from sensors import AudioSensor, MotionSensor, BleSensor
from expression_manager import ExpressionManager

class Controller:
    def __init__(self, audioSensor:AudioSensor, motionSensor:MotionSensor, bleSensor:BleSensor,
                 expression_manager: ExpressionManager, display) -> None:
        self._audioSensor = audioSensor
        self._motionSensor = motionSensor
        self._bleSensor = bleSensor
        self._expression_manager = expression_manager
        self._display = display

        self._expression_name:str = "basic"
        self._eyeIndex = 0
        self._mouthIndex = 0
        self._expression_now = None
        self._return_to_base_cooldown = 5
        self._cooldown_start = 0

        self._last_blink_time = time.monotonic()
        self._blink_time_duration = random.uniform(0.25, 0.5)

        self._expression_now = self._expression_manager.get_expression_io(self._expression_name, self._eyeIndex, self._mouthIndex)
        self._display.show(self._expression_now)


    def loop_once(self) -> None:
        self.check_ble_update()
        self.check_motion_update()
        self.blink_update()
        self.speak_update()

        self.update_expression()
    
    def blink_update(self):
        NOW = time.monotonic()
        if NOW - self._last_blink_time > self._blink_time_duration:
            self._last_blink_time = NOW
            self._blink_time_duration = random.uniform(0.15, 0.3)

            eyes_num = self._expression_manager.get_expression_info(self._expression_name)["eyes_num"]
            if eyes_num > 1:
                self._eyeIndex = (self._eyeIndex + 1) % eyes_num

    def speak_update(self):
        speaking = self._audioSensor.get_speaking_level()
        mouths_num = self._expression_manager.get_expression_info(self._expression_name)["mouths_num"]
        self._mouthIndex = speaking % mouths_num

    def update_expression(self):
        # !!!do not use except at the end of loop_once
        self._expression_now = self._expression_manager.get_expression_io(self._expression_name, self._eyeIndex, self._mouthIndex)
        self._display.show(self._expression_now)

    def check_ble_update(self):
        ble_input = self._bleSensor.read_ble_if_able()
        if ble_input != "":
            if self._expression_manager.has(ble_input):
                self._expression_name = ble_input
                self._eyeIndex = 0
                self._mouthIndex = 0
            else:
                self._bleSensor.write_ble_if_able("No such expression: " + ble_input + "\n")
                print(ble_input)

    def check_motion_update(self):
        direction = self._motionSensor.get_direction()
        print(direction)
        if direction == "up":
            self.change_expression("smile")
        elif direction == "down":
            self.change_expression("smile")
        elif direction == "left":
            self.change_expression("heart")
        elif direction == "right":
            self.change_expression("heart")
        else:
            if self._expression_name != "basic" and time.monotonic() - self._cooldown_start > self._return_to_base_cooldown:
                self.change_expression("basic")
                
        
        
    def change_expression(self, name:str):
        if self._expression_name == name:
            return
        else:
            self._expression_name = name
            self._eyeIndex = 0
            self._mouthIndex = 0
            if name != "basic":
                self._cooldown_start = time.monotonic()
            