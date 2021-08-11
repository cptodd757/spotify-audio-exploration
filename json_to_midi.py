import os
import binascii
import numpy as np
header_chunk = '4D 54 68 64 00 00 00 06 00 00 00 01 00 60'
MTrk = '4D 54 72 6B'
EOF = '00 FF 2F 00'
TICKDIV = 96
NUM_BEATS_USED = 10
NUM_SEGMENTS_USED = 500
LOWEST_NOTE = 6

def unhexlify(hex_string):
    #print(hex_string)
    return binascii.unhexlify(hex_string.replace(' ',''))

def to_hex_string(integer):
    return str(hex(integer)).replace('0x','').replace('L','').upper()

#make sure pitches are in right register (enforce LOWEST_NOTE)
def transpose(note):
    if note - 60 < LOWEST_NOTE:
        return note + 12
    return note

#represent deltatime properly.  if bigger than 127, add the extra byte in front.  integer is decimal
#DANGER: is assuming the integer is NOT greater than 256
def represent_dt(integer):
    if integer > 127:
        return '81' + to_hex_string(integer - 128)
    return to_hex_string(integer)

def convert(analysis, title='untitled'):
    f = open('data/' + title + '.mid', "w")

    f.write(unhexlify(header_chunk))
    f.write(unhexlify(MTrk))

    BEAT_LENGTH = np.sum([beat["duration"] for beat in analysis["beats"][:NUM_BEATS_USED]])/NUM_BEATS_USED
    MAX_LOUDNESS = np.amax([segment["loudness_max"] for segment in analysis["segments"]])
    MIN_LOUDNESS = np.amin([segment["loudness_max"] for segment in analysis["segments"]])

    hex_list = []
    end_prev = 0
    for segment in analysis['segments'][:NUM_SEGMENTS_USED]:
        def create_event(deltatime, note_on, channel, note, velocity):
            ans = ' '.join([
                represent_dt(int(np.round(deltatime))).zfill(2),
                ('9' if note_on else '8') + str(channel),
                to_hex_string(transpose(note)),
                to_hex_string(velocity).zfill(2)
            ])
            return ans

        note = np.argmax(segment["pitches"]) + 60
        velocity = int((segment["loudness_max"] - MIN_LOUDNESS)/(MAX_LOUDNESS - MIN_LOUDNESS) * 127)

        note_on_event = create_event(
            deltatime=segment["start"]/BEAT_LENGTH * TICKDIV - end_prev, 
            note_on=True, 
            channel=0, 
            note=note, 
            velocity=velocity)

        note_off_event = create_event(
            deltatime=segment["duration"]/BEAT_LENGTH * TICKDIV, 
            note_on=False, 
            channel=0, 
            note=note, 
            velocity=velocity)

        end_prev = (segment["start"] + segment["duration"])/BEAT_LENGTH * TICKDIV

        hex_list.append(note_on_event)
        hex_list.append(note_off_event)

    chunklen = unhexlify(to_hex_string(4 * (1 + len(hex_list))).zfill(8))
    f.write(chunklen)

    for line in hex_list:
        f.write(unhexlify(line))
    
    f.write(unhexlify(EOF))