import os

class Controller:
    def __init__(self):
        self.status = 0
        self.command = ''

    def playMusic(self, fileName):
        fileName = self.normalize(fileName)
        self.command = "open -a /Applications/iTunes.app " + fileName
        os.system(self.command)

    def playVideo(self, fileName):
        fileName = self.normalize(fileName)
        self.command = "open -a /Applications/IINA.app " + fileName
        os.system(self.command)

    def openNotepad(self):
        self.command = "open -a /Applications/Typora.app"
        os.system(self.command)

    def shutdown(self):
        self.command = "sudo halt"
        os.system(self.command)

    def normalize(self, fileName):
        beginPosition = fileName.find(" ", 0)
        while (beginPosition != -1):
            list_fileName = list(fileName)
            list_fileName.insert(beginPosition, '\\')
            fileName = "".join(list_fileName)
            beginPosition = fileName.find(" ", beginPosition+2)
        return fileName


if __name__ == "__main__":
    c = Controller()
    print(c.normalize("test normalization of text"))





# os.system('open -a /Applications/iTunes.app /Users/leon/Music/网易云音乐/Thomas\ Greenberg\ -\ The\ Human\ Touch.mp3')

# os.system('ls')