from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import *
import time

from asrInterface import Ui_MainWindow
import sys

import pyttsx3
import speech_recognition as sr
from controller import Controller

# 继承QThread
class Runthread(QtCore.QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self, mywindow):
        super(Runthread, self).__init__()
        self.mw = mywindow

    def __del__(self):
        self.wait()

    def run(self):
        speech_interaction(self.mw)
        # self._signal.emit("run")  # 信号发送


class myWindow(QtWidgets.QMainWindow):
    text = ""

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)





def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_sphinx(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def speech_interaction(mywindow):

    # 初始化pyttsx3 engine
    # engine = pyttsx3.init()
    # engine.say("请问您需要什么帮助？")
    # engine.runAndWait()

    # obtain audio from the microphone
    # 从麦克风记录数据
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # engine.say("请问您需要什么帮助？")
        # engine.runAndWait()
        guess = recognize_speech_from_mic(r, sr.Microphone())
        # guess["transcription"] = "play video"
        print("You said: {}".format(guess["transcription"]))
        mywindow.ui.updateL5("You said: {}".format(guess["transcription"]))



    # engine.say("录音结束, 识别中")
    # engine.runAndWait()

    c = Controller()



    if (guess["transcription"] == "play music"):
        c.playMusic("The Human Touch.mp3")
    if (guess["transcription"] == "play video"):
        c.playMusic("Lillard.mp4")
        mywindow.ui.updateL6("Opening Video by IINA...")
    elif(guess["transcription"] == "open note pad"):
        c.openNotepad()
        mywindow.ui.updateL6("Opening Typora...")
    elif(guess["transcription"] == "shutdown"):
        c.shutdown()
        mywindow.ui.updateL6("Shutdown...")
    else:
        mywindow.ui.updateL6("I can't do this...")



engine = pyttsx3.init()

app = QtWidgets.QApplication([])
application = myWindow()
application.show()

# engine = pyttsx3.init()
# engine.say("请问您需要什么帮助？")
# engine.runAndWait()

thread = Runthread(application)
thread.start()
sys.exit(app.exec())



