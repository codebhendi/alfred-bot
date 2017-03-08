import RPi.GPIO as gpio

class Light:
    def __init__(self):
        self.STATUS = False
	gpio.setmode(gpio.BCM)
	gpio.setwarnings(False)
	gpio.setup(18,gpio. OUT)

    def on_light(self):
        print("on")
	gpio.output(18, gpio.HIGH)
        self.STATUS = True

    def off_light(self):
        print("off")
	gpio.output(18, gpio.LOW)
        self.STATUS = False

    def check_command(self, data):
        if "on" in data:
            if self.STATUS == False:
                self.on_light()
            else :
                return "already on"
        elif "off" in data:
            if self.STATUS == False:
                self.off_light()
            else :
                return "already off"
