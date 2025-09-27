from gpiozero import DistanceSensor

def is_active(distance, activeDistance):
    return distance < activeDistance

def listen(triggerPin, echoPin, activeDistance, onEnterActiveRange, onWithinActiveRange, onLeaveActiveRange):
    ds = DistanceSensor(echo=echoPin, trigger=triggerPin)
    prevDist = ds.distance
    while True:
        distance = ds.distance
        if is_active(distance, activeDistance) and not is_active(prevDist, activeDistance):
            onEnterActiveRange(distance)

        elif is_active(distance, activeDistance) and is_active(prevDist, activeDistance):
            onWithinActiveRange(distance)

        elif not is_active(distance, activeDistance) and is_active(prevDist, activeDistance):
            onLeaveActiveRange(distance)
        
