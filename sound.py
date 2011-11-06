import pygame

class Sound:
    def __init__(self, audio_url):
        self.audio_url = audio_url

    def play(self):
        pygame.mixer.music.load(self.audio_url)
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()
