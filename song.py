import vlc

class Song:

    def __init__(self, speaker):
        self.mediadir = ""
        self.fname = "playlist.txt"
	self.speaker = speaker        

        with open(self.fname) as f:
            self.content = f.readlines()

        self.content = [x.strip() for x in self.content]


    def play(self, number=0):
	if self.status == False:
        	name = self.content[0]
        	self.player = vlc.MediaPlayer(name)
		self.player.play()
        	self.status = True
	else:
		self.stop()
		self.play()

    def stop(self):
	if self.status == True:
        	self.player.stop()
        	self.status = False
	else:
		self.speaker.say("you are not playing any songs right now")

    def check_command(self, data):
        if "play" in data:
            self.play()
        elif "stop" in data:
            self.stop()
