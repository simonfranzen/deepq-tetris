from pygame import mixer  # Load the popular external library


class AudioPlayer:

    def __init__(self):
        mixer.init()
        mixer.music.load('assets/tetris.ogg')

    def play(self):
        mixer.music.play(-1)

    def stop(self):
        mixer.music.stop()
