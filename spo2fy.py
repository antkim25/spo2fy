# Import libraries
import time, random, os, shutil
from pygame import mixer
from threading import Thread

# Randomizer for shuffle
sys_random = random.SystemRandom()
mixer.init()

# Music Player Class
class Player:
    version = 2.4
    paused = False
    playlist = ""
    curSong = ""
    looping = False
    playlistSize = 0
    volume = 0.5

    # Starting Instructions & Playlist Selecting
    def __init__(self):
        self.printInstructions()

        self.playlist = input("Select Playlist: ")
        while self.playlist not in os.listdir("playlists"):
            self.playlist = input("Playlist not found, try again: ")
        
    # Printing instructions/commands
    def printInstructions(self):
        print("----------------------------")
        print("Spo2fy (Version Beta " + str(self.version) + ")")
        print("----------------------------")
        print("All Commands")
        print("Change Playlists: c")
        print("Current Song: ?")
        print("Favorite/Unfavorite Current Song: f")
        print("Instructions/Help: h")
        print("Pause: p")
        print("Quit: q")
        print("Skip: s")
        print("Toggle: t")
        print("Toggle Loop: l")
        print("Unpause: u")
        print("Volume Down/Up: </>")
        print("----------------------------")

    # Returns size of given playlist
    def getPlaylistSize(self, p):
        size = 0
        for path in os.scandir("playlists/"+p):
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
        newSong = sys_random.choice(os.listdir("playlists/"+self.playlist))

        # Ensures "no song twice in a row" doesn't apply for one-song playlists
        if self.getPlaylistSize(self.playlist) != 1:
            # No song will play twice in a row
            while newSong == self.curSong:
                newSong = sys_random.choice(os.listdir("playlists/"+self.playlist))
        self.curSong = newSong
    
    # Returns path of song given song name and playlist
    def songPathMaker(self, song):
        return "playlists/" + self.playlist + "/" + song
    
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
        mixer.music.set_volume(self.volume)
        mixer.music.play()

        # Prints the currently playing message (if not looping)
        if not self.looping:
            print("Currently Playing: " + self.songFormat(self.curSong))

    # Checking for input
    def inputChecker(self):
        while True:
            # Input from user
            inp = input()

            # Pausing
            if (inp in ["Pause", "pause", "P", "p"]):
                self.pause()

            # Unpausing
            elif (inp in ["Unpause", "unpause", "U", "u", "Play", "play"]):
                self.unpause()

            # Toggling for Playing/Pausing
            elif (inp in ["Toggle", "toggle", "T", "t"]):
                if mixer.music.get_busy():
                    self.pause()
                else:
                    self.unpause()

            # Toggling for Looping
            elif (inp in ["Loop", "loop", "L", "l"]):
                if self.looping:
                    print("No longer looping: " + self.songFormat(self.curSong))
                else:
                    print("Now looping: " + self.songFormat(self.curSong))
                self.looping = not self.looping

            # What song is currently playing
            elif (inp in ["?", "Current", "current", "Cur", "cur"]):
                if self.looping:
                    print("(Playlist: " + self.playlist + "): Currently Looping: " + self.songFormat(self.curSong))
                else:
                    print("(Playlist: " + self.playlist + "): Currently Playing: " + self.songFormat(self.curSong))

            # Skipping
            elif (inp in ["Skip", "skip", "S", "s"]):
                print("Skipped!")
                self.songPlayer()

            # Changing Playlists
            elif (inp in ["Change", "change", "C", "c"]):
                self.playlist = input("Select playlist you'd like to switch to: ")
                while self.playlist not in os.listdir("playlists/"):
                    self.playlist = input("Playlist not found, try again: ")
                print("Changed playlist to " + self.playlist)
                self.songPlayer()

            # Favoriting Songs
            elif (inp in ["Favorite", "favorite", "F", "f"]):
                song = self.songFormat(self.curSong)
                self.favorite(song)
            
            # Displaying information menu
            elif (inp in ["Help", "help", "Info", "info", "H", "h", "I", "i"]):
                self.printInstructions()

            # Volume Change
            elif inp == ">":
                if round(self.volume + 0.1, 1) <= 1:
                    mixer.music.set_volume(round(self.volume + 0.1, 1))
                    self.volume = round(self.volume + 0.1, 1)
                    print("Volume Changed to:", self.volume)
            elif inp == "<":
                if round(self.volume - 0.1, 1) >= 0:
                    mixer.music.set_volume(round(self.volume - 0.1, 1))
                    self.volume = round(self.volume - 0.1, 1)
                    print("Volume Changed to:", self.volume)

            # Quitting program
            elif (inp in ["Exit", "exit", "Quit", "quit", "Q", "q", "E", "e"]):
                os._exit(1)
    
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

    # Favoriting
    def favorite(self, song):
        favesA = open("favorites.txt", "a")
        favesR = open("favorites.txt", "r")
        favesList = favesR.read()
        if song not in favesList:
            print("Favorited song!")
            if len(favesList) == 0:
                favesA.write(song)
            else:
                favesA.write("\n" + song)
            fp = open("playlists/favorited/" + self.curSong, 'x')
            fp.close()
            shutil.copyfile("playlists/" + self.playlist + "/" + self.curSong, "playlists/favorited/" + self.curSong)
        else:
            print("Unfavorited song!")
            newFaves = open("newFaves.txt", "x")
            newFaves.close()
            newFavesA = open("newFaves.txt", "a")
            favesR = open("favorites.txt", "r")
            lines = favesR.readlines()

            if len(lines) == 2 and lines[0][:-1] == song:
                newFavesA.write(lines[1][:-1])

            elif len(lines) != 1:
                # Added means whether or not the first line was added
                added = False
                if lines[0][:-1] != song:
                    newFavesA.write(lines[0][:-1])
                    added = True
                for i in range (1,len(lines) - 1):
                    if lines[i][:-1] != song:
                        if not added:
                            newFavesA.write(lines[i][:-1])
                            added = True
                        else:
                            newFavesA.write("\n" + lines[i][:-1])
                if lines[len(lines) - 1] != song:
                    newFavesA.write("\n" + lines[len(lines) - 1])

            newFavesA.close()
            favesR.close()

            shutil.copy2("newFaves.txt", "favorites.txt")
            os.remove("newFaves.txt")
            os.remove("playlists/favorited/" + self.curSong)

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