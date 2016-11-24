import pygame

#PLAY AUDIO CLIP
def play_audio(clip_to_play):
    print('play audio start')
    pygame.mixer.init()
    pygame.mixer.music.load(clip_to_play)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
      continue