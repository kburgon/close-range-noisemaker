from datetime import datetime, timedelta

from pydub.audio_segment import extract_wav_headers
import logger
import distance_listener
from sound_playback_helper import sound_player

dbName = 'events.db'
last_time_within_range = datetime.now()

def onEnterActiveRange(distance: int) -> None:
    logger.log_event('enter_range', distance, dbName)
    player = sound_player.SoundPlayer()
    player.play_rotated_sound()
    last_time_within_range = datetime.now()

def onWithinActiveRange(distance: int) -> None:
    logger.log_event('within_range', distance, dbName)
    cur_time = datetime.now()
    if last_time_within_range < cur_time - timedelta(seconds=60):
        player = sound_player.SoundPlayer()
        player.play_rotated_sound()

def onLeaveActiveRange(distance: int) -> None:
    logger.log_event('leave_range', distance, dbName)

if (__name__ == "__main__"):
    print('Started')
    trigger_pin = 7
    echo_pin = 11
    active_distance = 200
    distance_listener.listen(trigger_pin, echo_pin, active_distance, onEnterActiveRange, onWithinActiveRange, onLeaveActiveRange)
