import time, random, os
from pygame import mixer
sys_random = random.SystemRandom()
mixer.init()

playlist = "study"

def underscoreRemover(s):
    newS = ""
    for i in range (0, len(s)):
        if s[i] != "_":
            newS += s[i]
        else:
            newS += " "
    return newS

while True:
    song = sys_random.choice(os.listdir(playlist))
    songPath = playlist + "/" + song
    songSound = mixer.Sound(songPath)
    mixer.music.load(songPath)
    mixer.music.set_volume(0.7)
    mixer.music.play()

    leftParen = song.index("(")
    print("Currently Playing: " + underscoreRemover(song[0:leftParen]) + "by " + underscoreRemover(song[leftParen+1:-5]))

    time.sleep(songSound.get_length())