import pygame.mixer
import time
import random

pygame.mixer.init()

ambientSound = pygame.mixer.Sound("assets\\Sounds\\ambienceCave.ogg")

footstep = pygame.mixer.Sound("assets\\Sounds\\footstep.ogg")

stoneDrops = [
    pygame.mixer.Sound("assets\\Sounds\\stoneDropCave01.ogg"),
    pygame.mixer.Sound("assets\\Sounds\\stoneDropCave02.ogg"),
    pygame.mixer.Sound("assets\\Sounds\\stoneDropCave04.ogg")
]
waterDrips = [
    pygame.mixer.Sound("assets\\Sounds\\waterDripCave01.ogg")
]


horizons = "assets\\Music\\sb_horizons.ogg"
tearsInRain = "assets\\Music\\sb_tearsinrain.ogg"

class SoundManager:
    def __init__(self, randomSounds = True, ambience = True):
        Time = time.perf_counter()
        self.walk = Sounds(footstep, volume=0.015)
        self.walking = False
        self.walkTime = Time
        self.walkDelay = 0.75

        if ambience:
            Sounds(ambientSound, volume=0.15).play(-1)

        self.randomSounds = randomSounds 

        self.rockTime = Time
        self.rockDelay = random.randint(13000, 25000) / 1000

        self.waterDripTime = Time
        self.waterDripDelay = random.randint(3500, 4000) / 1000
        
    def startSound(self, walking = None, walkDelay = None):
        if walking != None:
            self.walking = walking
        if walkDelay != None:
            self.walkDelay = walkDelay
    
    def playSounds(self):
        Time = time.perf_counter()
        if self.walking and Time - self.walkTime > self.walkDelay:
            self.walk.play()
            self.walkTime = Time
        if self.randomSounds:
            if Time - self.rockTime > self.rockDelay:
                Sounds(stoneDrops[random.randrange(0,len(stoneDrops))], volume=0.15).play()
                self.rockTime = Time
                self.rockDelay = random.randint(13000, 25000) / 1000
            if Time - self.waterDripTime > self.waterDripDelay:
                Sounds(waterDrips[random.randrange(0,len(waterDrips))], volume=0.04).play()
                self.waterDripTime = Time
                self.waterDripDelay = random.randint(3500, 4000) / 1000

class Sounds:
    def __init__(self, sound, volume = 1):
        self.sound = sound
        self.sound.set_volume(volume)
        self.isPlaying = False
    
    def play(self, times = 0):
        if not self.sound.get_num_channels() >= 1:
            self.sound.play(times)
    
    def stop(self):
        self.sound.stop()

    def setVolume(self, volume):
        self.sound.set_volume(volume)
    
    def fadeOut(self, duration = 1000):
        self.sound.fadeout(duration)

class Music:
    def __init__(self, song, volume = 1, play = False, loop=False):
        pygame.mixer.music.load(song)
        pygame.mixer.music.set_volume(volume)
        if play:
            self.play(-1 if loop else 0)

    def setSong(self, song):
        pygame.mixer.music.load(song)
    
    def play(self, loops = 0):
        pygame.mixer.music.play(loops)

    def pause(self):
        pygame.mixer.music.pause()

    def setVolume(self, volume):
        pygame.mixer.music.set_volume(volume)

