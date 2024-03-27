import board
import busio
import adafruit_lis3dh
from math import atan, sqrt

class MotionSensor:
    def __init__(self):
        """
        Initializes a motion sensor object.
        """
        i2c = busio.I2C(board.SCL, board.SDA)  # Initialize I2C bus
        self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)  # Initialize LIS3DH sensor
        self.lis3dh.range = adafruit_lis3dh.RANGE_2_G  # Set range of accelerometer to 2G
        
    def get_acceleration(self):
        """
        Reads acceleration values from the sensor.

        Returns:
        - tuple: A tuple containing the acceleration values along the x, y, and z axes.
        """
        # Read acceleration values from the sensor and convert to Gs
        x, y, z = [value / adafruit_lis3dh.STANDARD_GRAVITY for value in self.lis3dh.acceleration]
        return x, y, z  # Return the acceleration values along the x, y, and z axes

    def get_direction_angle(self):
        """
        Calculates the angle of the direction of the acceleration vector.

        Returns:
        - tuple: A tuple containing the angles of the direction of the acceleration vector along the x, y, and z axes.
        """
        x, y, z = self.get_acceleration()
        angle_x = atan(x/sqrt(y*y+z*z)) * 180 / 3.14
        angle_y = atan(y/sqrt(x*x+z*z)) * 180 / 3.14
        angle_z = atan(z/sqrt(x*x+y*y)) * 180 / 3.14
        return angle_x, angle_y, angle_z
    
    def get_direction(self):
        angle_x, angle_y, angle_z = self.get_direction_angle()
        if angle_x > 45:
            return "up"
        elif angle_x < -45:
            return "down"
        elif angle_y > 45:
            return "right"
        elif angle_y < -45:
            return "left"
        elif angle_z > 45:
            return "front"
        elif angle_z < -45:
            return "back"
        else:
            return "stationary"