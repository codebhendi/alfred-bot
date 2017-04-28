class Light:
    def __init__(self):
        self.STATUS = False

    def on_light(self):
        print("on")
        self.STATUS = True

    def off_light(self):
        print("off")
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