import vlc

class Song:

    def __init__(self):
        self.mediadir = ""
        self.fname = "playlist.txt"
        
        with open(self.fname) as f:
            self.content = f.readlines()

        self.content = [x.strip() for x in self.content]


    def play(self, number=0):

        name = self.content[0]
        self.player = vlc.MediaPlayer(name)
        self.player.play()
        self.status = True

    def stop(self):
        self.player.stop()
        self.status = False

    def check_command(self, data):
        if "play" in data:
            self.play()
        elif "stop" in data:
            self.stop()