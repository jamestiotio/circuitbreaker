# coding: utf-8
# Since external libraries are not allowed for this assignment, I need to implement my own cross-platform audio system using only standard Python libraries
# Slightly modified from https://github.com/TaylorSMarks/playsound
# Created by James Raphael Tiovalen (2020)

def _playaudioWin(sound, block=True):
    '''
    Utilizes windll.winmm.
    '''
    from ctypes import c_buffer, windll
    from random import random
    from time import sleep
    from sys import getfilesystemencoding

    def winCommand(*command):
        buf = c_buffer(255)
        command = ' '.join(command).encode(getfilesystemencoding())
        errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
        if errorCode:
            errorBuffer = c_buffer(255)
            windll.winmm.mciGetErrorStringA(errorCode, errorBuffer, 254)
            exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
                                '\n        ' + command.decode() +
                                '\n    ' + errorBuffer.value.decode())
            raise Exception(exceptionMessage)
        return buf.value

    alias = 'playaudio_' + str(random())
    winCommand('open "' + sound + '" alias', alias)
    winCommand('set', alias, 'time format milliseconds')
    durationInMS = winCommand('status', alias, 'length')
    winCommand('play', alias, 'from 0 to', durationInMS.decode())

    # TODO: Improvement to be made would be to loop the audio without a blocking while loop

    if block:
        sleep(float(durationInMS) / 1000.0)
    
    return alias


def _stopaudioWin(alias):
    from ctypes import c_buffer, windll
    from random import random
    from time import sleep
    from sys import getfilesystemencoding

    def winCommand(*command):
        buf = c_buffer(255)
        command = ' '.join(command).encode(getfilesystemencoding())
        errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
        if errorCode:
            errorBuffer = c_buffer(255)
            windll.winmm.mciGetErrorStringA(errorCode, errorBuffer, 254)
            exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
                                '\n        ' + command.decode() +
                                '\n    ' + errorBuffer.value.decode())
            raise Exception(exceptionMessage)
        return buf.value
    
    winCommand('close', alias)


def _playaudioOSX(sound, block=True):
    '''
    Utilizes AppKit.NSSound.
    '''
    from AppKit import NSSound
    from Foundation import NSURL
    from time import sleep

    if '://' not in sound:
        if not sound.startswith('/'):
            from os import getcwd
            sound = getcwd() + '/' + sound
        sound = 'file://' + sound
    url = NSURL.URLWithString_(sound)
    nssound = NSSound.alloc().initWithContentsOfURL_byReference_(url, True)
    if not nssound:
        raise IOError('Unable to load sound named: ' + sound)
    nssound.play()

    if block:
        sleep(nssound.duration())


def _playaudioUnix(sound, block=True):
    '''
    Play a sound using GStreamer.
    '''
    if not block:
        raise NotImplementedError(
            "block=False cannot be used on this platform yet")

    # pathname2url escapes non-URL-safe characters
    import os
    try:
        from urllib.request import pathname2url
    except ImportError:
        # python 2
        from urllib import pathname2url

    import gi
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst

    Gst.init(None)

    playbin = Gst.ElementFactory.make('playbin', 'playbin')
    if sound.startswith(('http://', 'https://')):
        playbin.props.uri = sound
    else:
        playbin.props.uri = 'file://' + pathname2url(os.path.abspath(sound))

    set_result = playbin.set_state(Gst.State.PLAYING)
    if set_result != Gst.StateChangeReturn.ASYNC:
        raise Exception(
            "playbin.set_state returned " + repr(set_result))

    # TODO: use some other bus method than poll() with block=False
    # https://lazka.github.io/pgi-docs/#Gst-1.0/classes/Bus.html
    bus = playbin.get_bus()
    bus.poll(Gst.MessageType.EOS, Gst.CLOCK_TIME_NONE)
    playbin.set_state(Gst.State.NULL)


from platform import system
system = system()

if system == 'Windows':
    playaudio = _playaudioWin
elif system == 'Darwin':
    playaudio = _playaudioOSX
else:
    playaudio = _playaudioUnix

stopaudio = _stopaudioWin  # Need to make this cross-platform as well

del system
