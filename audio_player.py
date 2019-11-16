from pygame import mixer

""" a module handling the audio output of the application"""

class AudioPlayer:
    """a class that plays music"""

    def __init__(self):
        mixer.init()
        mixer.music.load('assets/tetris.ogg')

    def play(self):
        mixer.music.play(-1)

    def stop(self):
        mixer.music.stop()
