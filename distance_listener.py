from datetime import datetime
from typing import Callable
import RPi.GPIO as GPIO
import time

class DistanceListener:
    def __init__(self, triggerPin: int, echoPin: int, activeDistanceCm: int, checkFrequencySec: float, retriggerFrequencySec: float) -> None:
        self.trigger_pin = triggerPin
        self.echo_pin = echoPin
        self.active_distance_cm = activeDistanceCm
        self.check_frequency_sec = checkFrequencySec
        self.retrigger_frequency_sec = retriggerFrequencySec
        self.last_active_time = datetime.today()

    def is_active(self, distance: int) -> bool:
        return distance < self.active_distance_cm

    def setup_sensor(self, onError: Callable[[Exception], None]) -> None:
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.trigger_pin, GPIO.OUT)
            GPIO.setup(self.echo_pin, GPIO.IN)
            GPIO.output(self.trigger_pin, GPIO.LOW)
            print('Letting sensor settle')
            time.sleep(2)
            print('Sensor ready')
        except Exception as e:
            onError(e)

    def read_distance(self, onReadError: Callable[[Exception], None]) -> int:
        try:
            GPIO.output(self.trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.trigger_pin, GPIO.LOW)
            pulse_start_time = pulse_end_time = 0

            while GPIO.input(self.echo_pin) == 0:
                pulse_start_time = time.time()
            while GPIO.input(self.echo_pin) == 1:
                pulse_end_time = time.time()

            duration = pulse_end_time - pulse_start_time
            distance = round(duration * 17150, 2)
            return int(distance)
        except Exception as e:
            onReadError(e)
            return 0

    def listen(self, onEnterActiveRange: Callable[[int], None], onWithinActiveRange: Callable[[int], None], onLeaveActiveRange: Callable[[int], None], onError: Callable[[Exception], None]) -> None:
        self.setup_sensor(onError)
        prevDist = self.read_distance(onError)
        while True:
            distance = self.read_distance(onError)
            curTime = datetime.now()
            timeFromLastTime = curTime - self.last_active_time
            if self.is_active(distance) and not self.is_active(prevDist) and timeFromLastTime.seconds > self.retrigger_frequency_sec:
                onEnterActiveRange(distance)
                self.last_active_time = curTime

            elif self.is_active(distance) and self.is_active(distance) and timeFromLastTime.seconds > self.retrigger_frequency_sec:
                onWithinActiveRange(distance)
                self.last_active_time = curTime

            elif not self.is_active(distance) and self.is_active(distance):
                onLeaveActiveRange(distance)

            prevDist = distance
            time.sleep(self.check_frequency_sec)
            
    def close(self) -> None:
        GPIO.cleanup()
