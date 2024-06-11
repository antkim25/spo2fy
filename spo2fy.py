# Import libraries
import time, random, os
from pygame import mixer
from threading import Thread

# Randomizer for shuffle
sys_random = random.SystemRandom()
mixer.init()

# Music Player Class
class Player:
    paused = False
    playlist = ""
    curSong = ""
    looping = False
    playlistSize = 0

    # Starting Instructions & Playlist Selecting
    def __init__(self):
        print("------------------")
        print("Spo2fy Version 1.5")
        print("------------------")
        print("Basic Commands")
        print("Pause: p")
        print("Unpause: u")
        print("Toggle: t")
        print("Toggle Loop: l")
        print("Skip: s")
        print("Current Song: ?")
        print("------------------")

        self.playlist = input("Select Playlist: ")

    # Returns size of given playlist
    def getPlaylistSize(self, p):
        size = 0
        for path in os.scandir(p):
            if path.is_file():
                size += 1
        return size

    # Formatter for turning file name separated by underscores into one separated by spaces
    def underscoreRemover(self, s):
        newS = ""
        for i in range (0, len(s)):
            if s[i] != "_":
                newS += s[i]
            else:
                newS += " "
        return newS
    
    # Randomly picks song
    def songPicker(self):
        newSong = sys_random.choice(os.listdir(self.playlist))

        # Ensures "no song twice in a row" doesn't apply for one-song playlists
        if self.getPlaylistSize(self.playlist) != 1:
            # No song will play twice in a row
            while newSong == self.curSong:
                newSong = sys_random.choice(os.listdir(self.playlist))
        self.curSong = newSong
    
    # Returns path of song given song name and playlist
    def songPathMaker(self, song):
        return self.playlist + "/" + song
    
    # Returns formatted message for song title and artist
    def songFormat(self, song):
        leftParen = song.index("(")
        return self.underscoreRemover(song[0:leftParen]) + "by " + self.underscoreRemover(song[leftParen+1:-5])

    # Main loop for playing songs
    def songPlayer(self):
        # Pick a new song if it's not looping
        if not self.looping:
            self.songPicker()
        
        # Load song into mixer and play
        songPath = self.songPathMaker(self.curSong)
        mixer.music.load(songPath)
        mixer.music.set_volume(0.7)
        mixer.music.play()

        # Prints the currently playing message (if not looping)
        if not self.looping:
            print("Currently Playing: " + self.songFormat(self.curSong))

    # Checking for input
    def inputChecker(self):
        while True:
            # Input from user
            x = input()

            # Pausing
            if (x in ["Pause", "pause", "P", "p"]):
                self.pause()

            # Unpausing
            elif (x in ["Unpause", "unpause", "U", "u", "Play", "play"]):
                self.unpause()

            # Toggling for Playing/Pausing
            elif (x in ["Toggle", "toggle", "T", "t"]):
                if mixer.music.get_busy():
                    self.pause()
                else:
                    self.unpause()

            # Toggling for Looping
            elif (x in ["Loop", "loop", "L", "l"]):
                if self.looping:
                    print("No longer looping: " + self.songFormat(self.curSong))
                else:
                    print("Now looping: " + self.songFormat(self.curSong))
                self.looping = not self.looping

            # What song is currently playing
            elif (x in ["?", "Current", "current", "Cur", "cur"]):
                print("Currently Playing: " + self.songFormat(self.curSong))

            # Skipping
            elif (x in ["Skip", "skip", "S", "s"]):
                print("Skipped!")
                self.songPlayer()
    
    # Pausing
    def pause(self):
        self.paused = True
        print("Paused!")
        mixer.music.pause()

    # Unpausing
    def unpause(self):
        self.paused = False
        print("Unpaused!")
        mixer.music.unpause()

    # Automatically plays next song when song is over
    def playChecker(self):
        while True:
            time.sleep(1)
            if not self.paused and not mixer.music.get_busy():
                self.songPlayer()

# Initialize the music player
player = Player()

# Set up threads to run concurrently
songPlay = Thread(target = player.songPlayer)
inputCheck = Thread(target = player.inputChecker)
playCheck = Thread(target = player.playChecker)
songPlay.start()
inputCheck.start()
playCheck.start()