import time, random, os
from pygame import mixer
from threading import Thread

sys_random = random.SystemRandom()
mixer.init()

playlist = "study"

class Player:
    def __init__(self, paused):
        print("----------------------------")
        print("Spotify 2 (Version Beta 1.0)")
        print("----------------------------")
        print("Basic Commands")
        print("Pause: p")
        print("Unpause: u")
        print("Toggle: t")
        print("Skip: s")
        print("----------------------------")
        self.paused = paused

    def underscoreRemover(self, s):
        newS = ""
        for i in range (0, len(s)):
            if s[i] != "_":
                newS += s[i]
            else:
                newS += " "
        return newS

    def songPick(self):
        song = sys_random.choice(os.listdir(playlist))
        songPath = playlist + "/" + song
        return song, songPath

    def songPlayer(self):
        song, songPath = self.songPick()
        mixer.music.load(songPath)
        mixer.music.set_volume(0.7)
        mixer.music.play()

        leftParen = song.index("(")
        print("Currently Playing: " + self.underscoreRemover(song[0:leftParen]) + "by " + self.underscoreRemover(song[leftParen+1:-5]))

    def skip(self):
        song, songPath = self.songPick()
        mixer.music.load(songPath)
        mixer.music.set_volume(0.7)
        mixer.music.play()

        leftParen = song.index("(")
        print("Currently Playing: " + self.underscoreRemover(song[0:leftParen]) + "by " + self.underscoreRemover(song[leftParen+1:-5]))


    def inputChecker(self):
        while True:
            time.sleep(1.1)
            x = input()
            if (x == "Pause" or x == "pause" or x == "p"):
                self.paused = True
                print("Paused!")
                mixer.music.pause()
            elif (x == "Unpause" or x == "unpause" or x == "u"):
                self.paused = False
                print("Unpaused!")
                mixer.music.unpause()
            elif (x == "T" or x == "t"):
                if mixer.music.get_busy():
                    self.paused = True
                    print("Paused!")
                    mixer.music.pause()
                else:
                    self.paused = False
                    print("Unpaused!")
                    mixer.music.unpause()
            elif (x == "Skip" or x == "skip" or x == "s"):
                print("Skipped!")
                self.skip()

    def playChecker(self):
        while True:
            time.sleep(1)
            if not self.paused and not mixer.music.get_busy():
                self.skip()

paused = False
player = Player(paused)
songPlay = Thread(target = player.songPlayer)
inputCheck = Thread(target = player.inputChecker)
playCheck = Thread(target = player.playChecker)
songPlay.start()
inputCheck.start()
playCheck.start()