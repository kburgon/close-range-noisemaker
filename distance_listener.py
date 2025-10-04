from typing import Callable
from gpiozero import DistanceSensor

def is_active(distance, activeDistance):
    return distance < activeDistance

def listen(triggerPin: int, echoPin: int, activeDistance: int, onEnterActiveRange: Callable[[int], None], onWithinActiveRange: Callable[[int], None], onLeaveActiveRange: Callable[[int], None]) -> None:
    ds = DistanceSensor(echo=echoPin, trigger=triggerPin)
    prevDist = ds.distance * 100 # Convert the distance from meters to centimeters
    while True:
        distance = int(ds.distance)
        if is_active(distance, activeDistance) and not is_active(prevDist, activeDistance):
            onEnterActiveRange(distance)

        elif is_active(distance, activeDistance) and is_active(prevDist, activeDistance):
            onWithinActiveRange(distance)

        elif not is_active(distance, activeDistance) and is_active(prevDist, activeDistance):
            onLeaveActiveRange(distance)
        
