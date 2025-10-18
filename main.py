import logger
from distance_listener import DistanceListener
from sound_playback_helper.sound_player import SoundPlayer

dbName = 'events.db'

def onEnterActiveRange(distance: int) -> None:
    logger.log_event('enter_range', distance, dbName)
    player = SoundPlayer()
    player.all_sounds = player.list_sounds()
    player.play_rotated_sound()

def onWithinActiveRange(distance: int) -> None:
    logger.log_event('within_range', distance, dbName)
    player = SoundPlayer()
    player.all_sounds = player.list_sounds()
    player.play_rotated_sound()

def onLeaveActiveRange(distance: int) -> None:
    logger.log_event('leave_range', distance, dbName)

def onError(exception: Exception) -> None:
    logger.log_event(f"error: {exception}", 0, dbName)

if (__name__ == "__main__"):
    print('Started')
    trigger_pin = 7
    echo_pin = 11
    active_distance_sec = 100
    check_frequency_sec = 0.25
    retrigger_frequency_sec = 10
    listener = DistanceListener(trigger_pin, echo_pin, active_distance_sec, check_frequency_sec, retrigger_frequency_sec)
    try:
        listener.listen(onEnterActiveRange, onWithinActiveRange, onLeaveActiveRange, onError)
    finally:
        listener.close()
