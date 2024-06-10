import time, random, os
from pygame import mixer
from threading import Thread

sys_random = random.SystemRandom()
mixer.init()

class Player:
    paused = False
    playlist = ""
    curSong = ""
    looping = False

    def __init__(self):
        print("----------------------------")
        print("Spo2fy (Version Beta 1.3)")
        print("----------------------------")
        print("Basic Commands")
        print("Pause: p")
        print("Unpause: u")
        print("Toggle: t")
        print("Toggle Loop: l")
        print("Skip: s")
        print("----------------------------")
        self.playlist = input("Select Playlist: ")

    def underscoreRemover(self, s):
        newS = ""
        for i in range (0, len(s)):
            if s[i] != "_":
                newS += s[i]
            else:
                newS += " "
        return newS
    
    def songPicker(self):
        newSong = sys_random.choice(os.listdir(self.playlist))
        while newSong == self.curSong:
            newSong = sys_random.choice(os.listdir(self.playlist))
        self.curSong = newSong
    
    def songPathMaker(self, song):
        return self.playlist + "/" + song
    
    def songFormat(self, song):
        leftParen = song.index("(")
        return self.underscoreRemover(song[0:leftParen]) + "by " + self.underscoreRemover(song[leftParen+1:-5])

    def songPlayer(self):
        if not self.looping:
            self.songPicker()
        
        songPath = self.songPathMaker(self.curSong)
        mixer.music.load(songPath)
        mixer.music.set_volume(0.7)
        mixer.music.play()

        print("Currently Playing: " + self.songFormat(self.curSong))

    def inputChecker(self):
        while True:
            time.sleep(1.1)
            x = input()
            if (x in ["Pause", "pause", "P", "p"]):
                self.pause()
            elif (x in ["Unpause", "unpause", "U", "u"]):
                self.unpause()
            elif (x in ["Toggle", "toggle", "T", "t"]):
                if mixer.music.get_busy():
                    self.pause()
                else:
                    self.unpause()
            elif (x in ["Loop", "loop", "L", "l"]):
                if self.looping:
                    print("No longer looping: " + self.songFormat(self.curSong))
                else:
                    print("Now looping: " + self.songFormat(self.curSong))
                self.looping = not self.looping
            elif (x in ["Skip", "skip", "S", "s"]):
                print("Skipped!")
                self.songPlayer()
    
    def pause(self):
        self.paused = True
        print("Paused!")
        mixer.music.pause()
    
    def unpause(self):
        self.paused = False
        print("Unpaused!")
        mixer.music.unpause()

    def playChecker(self):
        while True:
            time.sleep(1)
            if not self.paused and not mixer.music.get_busy():
                self.songPlayer()

player = Player()
songPlay = Thread(target = player.songPlayer)
inputCheck = Thread(target = player.inputChecker)
playCheck = Thread(target = player.playChecker)
songPlay.start()
inputCheck.start()
playCheck.start()