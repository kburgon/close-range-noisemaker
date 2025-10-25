import logger
from distance_listener import DistanceListener
from sound_playback_helper.sound_player import SoundPlayer

dbName = 'events.db'


class DistanceEvents:
    def __init__(self):
        self.sound_player = SoundPlayer()

    def onEnterActiveRange(self, distance: int) -> None:
        logger.log_event('enter_range', distance, dbName)
        self.sound_player.play_rotated_sound()

    def onWithinActiveRange(self, distance: int) -> None:
        logger.log_event('within_range', distance, dbName)
        self.sound_player.play_rotated_sound()

    def onLeaveActiveRange(self, distance: int) -> None:
        logger.log_event('leave_range', distance, dbName)

    def onError(self, exception: Exception) -> None:
        logger.log_event(f"error: {exception}", 0, dbName)


if (__name__ == "__main__"):
    print('Started')
    trigger_pin = 7
    echo_pin = 11
    active_distance_sec = 100
    check_frequency_sec = 0.25
    retrigger_frequency_sec = 10
    de = DistanceEvents()
    listener = DistanceListener(trigger_pin, echo_pin, active_distance_sec, check_frequency_sec, retrigger_frequency_sec)
    try:
        listener.listen(de.onEnterActiveRange, de.onWithinActiveRange, de.onLeaveActiveRange, de.onError)
    finally:
        listener.close()
