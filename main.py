import logger
import distance_listener
from sound_playback_helper import sound_player
# Steps

# Create sensor module - done

# Establish distance listener - done

# Give distance listener events for entered range, within range, and left range events - done

# Create event logger - done

# Create event methods to call

# Within event methods, create event logging, sound actions
dbName = 'events.db'

def onEnterActiveRange(distance):
    logger.log_event('enter_range', distance, dbName)
    player = sound_player.SoundPlayer()
    player.play_rotated_sound()


if (__name__ == "__main__"):
    print('Started')
