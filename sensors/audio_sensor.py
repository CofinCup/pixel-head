import time
from analogio import AnalogIn

class AudioSensor:
    def __init__(self, pin):
        """
        Initializes an audio sensor object with the provided pin.

        Args:
        - pin (board.Pin): The pin connected to the analog audio sensor.

        Returns:
        - None
        """
        self.mic_pin = pin  # Store the pin connected to the audio sensor
        self.sampleWindow = 0.033  # Sample window width (0.033 sec = 33 mS = ~30 Hz)
        self.mic = AnalogIn(self.mic_pin)  # Initialize AnalogIn object for reading from the pin
    
    def get_audio_signal(self):
        """
        Reads audio signal from the sensor and calculates the peak-to-peak amplitude.

        Returns:
        - float: The peak-to-peak amplitude of the audio signal.
        """
        signalMin = 65535  # Initialize minimum signal value
        signalMax = 0      # Initialize maximum signal value
        start_time = time.monotonic()  # Record start time for sampling window
        # Loop to read audio signal within the sampling window
        while (time.monotonic() - start_time) < self.sampleWindow:
            signal = self.mic.value  # Read signal value from the sensor
            if signal < signalMin:
                signalMin = signal  # Update minimum signal value if necessary
            if signal > signalMax:
                signalMax = signal  # Update maximum signal value if necessary
        peakToPeak = signalMax - signalMin  # Calculate peak-to-peak amplitude
        return peakToPeak  # Return the peak-to-peak amplitude
    
    def get_speaking_level(self):
        speaking_level = int(((self.get_audio_signal() - 250) * 2) / 16383)  # Remove low-level noise, boost
        return speaking_level

