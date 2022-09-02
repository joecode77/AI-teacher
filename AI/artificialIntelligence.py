from PyQt5.QtCore import QThread, pyqtSignal
from vosk import Model, KaldiRecognizer
from PyDictionary import PyDictionary
import speech_recognition as sr
from playsound import playsound
from pydub.playback import play
from googlesearch import search
from pydub import AudioSegment
from bs4 import BeautifulSoup
import sounddevice as sd
import soundfile as sf
from gtts import gTTS
import wikipedia
import threading
import datetime
import requests
import random
import time
import gtts




playing = True
dictionary_result = None
wikipedia_result = None
google_result = None

dictionary_displayed = False
wikipedia_displayed = False
google_displayed = False

answer = None
in_thinking_process = False


class Speak(QThread):
    finshed = pyqtSignal()

    def __init__(self, label, change_icon_function):
        super().__init__()
        self.label = label
        self.change_icon_function = change_icon_function

    def run(self):
        global playing

        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.label.setText("Listening...")
            audio = r.listen(source)
            self.label.clear()
            self.change_icon_function()

        try:
            said = r.recognize_google(audio)
            # print("TEXT", said)
            self.routeText(said)

        except sr.RequestError:
            data, fs = sf.read("audio/no connection.wav")
            playing = True
            sd.play(data, fs)
            sd.wait()
            playing = False

        except sr.UnknownValueError:
            data, fs = sf.read("audio/not audible.wav")
            playing = True
            sd.play(data, fs)
            sd.wait()
            playing = False

    def define(self, text):
        self.dictionary_only = Dictionary(text, handle_errors=True)
        self.dictionary_only.start()

    def defineAndSearch(self, text):
        # print("ENTERED DEFINE AND SEARCH")
        self.dictionary = Dictionary(text, handle_errors=False)
        self.dictionary.start()

        self.wikipedia = Wikipedia(text)
        self.wikipedia.start()

        self.google_search = GoogleSearch(text)
        self.google_search.start()

        thinkingLogic()

    def questionAnswering(self, text):
        print("Question answered")

    def info(self, text):
        if "what is your name" in text or "tell me about yourself" in text or "who are you" in text:
            song = AudioSegment.from_mp3("audio/myself.mp3")
            playing = True
            play(song)
            playing = False

    def greeting(self, text):
        if "hello" in text or "hey" in text:
            song = AudioSegment.from_mp3("audio/hello.mp3")
            playing = True
            play(song)
            playing = False

        elif "hi" in text:
            song = AudioSegment.from_mp3("audio/hi.mp3")
            playing = True
            play(song)
            playing = False

        elif "how do you do" in text or "how have you been" in text or "how are you" in text or "what's up" in text:
            song = AudioSegment.from_mp3("audio/been good.mp3")
            playing = True
            play(song)
            playing = False

        elif "good morning" in text:
            song = AudioSegment.from_wav("audio/good morning.wav")
            playing = True
            play(song)
            playing = False

        elif "good afternoon" in text:
            song = AudioSegment.from_wav("audio/good afternoon.wav")
            playing = True
            play(song)
            playing = False

        elif "good evening" in text:
            song = AudioSegment.from_wav("audio/good evening.wav")
            playing = True
            play(song)
            playing = False
        
        elif "goodnight" in text:
            song = AudioSegment.from_mp3("audio/good night.mp3")
            playing = True
            play(song)
            playing = False
            exit()

        elif "good day" in text:
            song = AudioSegment.from_mp3("audio/good day.mp3")
            playing = True
            play(song)
            playing = False

        elif "i am good" in text or "i am doing good" in text or "i'm great" in text or "i am great" in text:
            song = AudioSegment.from_mp3("audio/that is great.mp3")
            playing = True
            play(song)
            playing = False

        elif "thanks" in text or "thank you" in text:
            options = ["audio/anytime.mp3", "audio/you are welcome.mp3"]
            option = random.choice(options)
            song = AudioSegment.from_mp3(option)
            playing = True
            play(song)
            playing = False

    def routeText(self, text):
        # print("ENTERED ROUTING")

        operations = {"hello": self.greeting, "hi": self.greeting, "how do you do": self.greeting, "how have you been": self.greeting, "good morning": self.greeting,
                      "good afternoon": self.greeting, "good evening": self.greeting, "goodnight": self.greeting, "good day": self.greeting, "hey": self.greeting, "what's up": self.greeting,
                      "thank you": self.greeting, "thanks": self.greeting, "how are you": self.greeting, "i'm good": self.greeting, "i'm doind good": self.greeting,
                      "i am good": self.greeting, "i am doing good": self.greeting, "i'm great": self.greeting, "i am great": self.greeting,
                      "what is your name": self.info, "tell me about yourself": self.info, "who are you": self.info,
                      "define": self.define, "define the term": self.define, "what is the meaning of": self.define,
                      "what is the meaning of the term": self.define, "what is": self.defineAndSearch, "explain": self.defineAndSearch,
                      "who is": self.defineAndSearch, "how to": self.defineAndSearch, "how do you": self.defineAndSearch,
                      "what are": self.defineAndSearch, "what was": self.defineAndSearch, "when was": self.questionAnswering, "how to": self.questionAnswering,
                      "how do you": self.questionAnswering, "can you": self.questionAnswering, "can i": self.questionAnswering, "can": self.questionAnswering,
                      "who": self.questionAnswering, "when": self.questionAnswering, "where": self.questionAnswering, "which": self.questionAnswering, "does": self.questionAnswering,
                      }

        for operation in operations:
            if operation in text:
                # print(operation)
                operations[operation](text)
                break

            else:
                global answer
                answer = text


class Wikipedia(QThread):
    finished = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.text = text
        # print("ENTERED WIKIPEDIA")

    def run(self):
        global wikipedia_result
        global playing
        try:
            summary = wikipedia.summary(self.text)

            filename = "audio/wikipedia.mp3"
            tts = gTTS(text=summary, lang="en", tld="com.au", slow=False)
            tts.save(filename)
            wikipedia_result = True
            # print("DONE WITH WIKI")

        except wikipedia.exceptions.PageError:
            wikipedia_result = False

        except requests.exceptions.ConnectionError:
            song = AudioSegment.from_wav("audio/no connection.wav")
            playing = True
            play(song)
            playing = False

        except gtts.tts.gTTSError:
            data, fs = sf.read("audio/no connection.wav")
            playing = True
            sd.play(data, fs)
            sd.wait()
            playing = False


class GoogleSearch(QThread):

    def __init__(self, text):
        super().__init__()
        self.query = text
        self.combined_info = ""
        self.API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        self.headers = {
            "Authorization": "Bearer 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"}
        # print("ENTERED GOOGLE")

    def run(self):
        global google_result
        global playing

        urls = search(self.query, tld="co.in", num=2,  stop=2, pause=2)
        urls = list(urls)

        t1 = threading.Thread(target=self.getFirstPageContent, args=(urls[0],))
        t2 = threading.Thread(
            target=self.getSecondPageContent, args=(urls[1],))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        def query(payload):
            global playing

            response = requests.post(
                self.API_URL, headers=self.headers, json=payload)
            return response.json()

        output = query({"inputs": self.combined_info, })

        output = output[0].get(
            "summary_text", "Sorry, i'm unable to get information at the moment")

        try:
            filename = "audio/google.mp3"
            tts = gTTS(text=output, lang="en", tld="com.au", slow=False)
            tts.save(filename)
            google_result = True
            # print("DONE WITH GOOGLE")

        except:
            data, fs = sf.read("audio/no connection.wav")
            playing = True
            sd.play(data, fs)
            sd.wait()
            playing = False

    def getFirstPageContent(self, url):
        global playing
        try:
            passage = ""
            response = requests.get(url).content
            soup = BeautifulSoup(response, 'html.parser')
            soup = soup.find_all('p')
            for i in soup:
                passage += i.get_text()

            self.combined_info += passage
        except requests.exceptions.ConnectionError:
            song = AudioSegment.from_wav("audio/no connection.wav")
            playing = True
            play(song)
            playing = False

    def getSecondPageContent(self, url):
        global playing
        try:
            passage = ""
            response = requests.get(url).content
            soup = BeautifulSoup(response, 'html.parser')
            soup = soup.find_all('p')
            for i in soup:
                passage += i.get_text()

            self.combined_info += passage
        except requests.exceptions.ConnectionError:
            song = AudioSegment.from_wav("audio/no connection.wav")
            playing = True
            play(song)
            playing = False


class Dictionary(QThread):
    finished = pyqtSignal()

    def __init__(self, text, handle_errors):
        super().__init__()
        self.text = text
        self.handle_errors = handle_errors
        # print("ENTERED DICTIONARY")

    def run(self):
        global playing
        global dictionary_result

        self.text = self.text.split()[-1]
        dictionary = PyDictionary()
        definition = [f"{self.text} is"]
        try:
            pairs = dictionary.meaning(self.text, disable_errors=True)
            pairs = pairs.values()
            for meaning in pairs:
                definition.append(
                    " or could also be defined as ".join(meaning))
            definition = " or could also be defined as ".join(definition)
            # print("DEFINITION", definition)

            filename = "audio/define.mp3"

            tts = gTTS(text=definition, lang="en", tld="com.au", slow=False)
            tts.save(filename)

            if self.handle_errors == True:
                song = AudioSegment.from_mp3(filename)
                playing = True
                play(song)
                playing = False
            else:
                dictionary_result = True
                # print("DONE WITH DICTIONARY")

        except gtts.tts.gTTSError:
            data, fs = sf.read("audio/no connection.wav")
            playing = True
            sd.play(data, fs)
            sd.wait()
            playing = False

        except:
            if self.handle_errors == True:
                # print("Error")
                data, fs = sf.read("audio/error.wav")
                playing = True
                sd.play(data, fs)
                sd.wait()
                playing = False
            else:
                dictionary_result = False


def thinkingLogic():
    # print("ENTERED THINKING LOGIC")
    global dictionary_result, dictionary_displayed, wikipedia_result, wikipedia_displayed, google_result, google_displayed
    global answer, playing, in_thinking_process

    in_thinking_process = True
    while True:
        if dictionary_result == True and dictionary_displayed == False:
            song = AudioSegment.from_mp3("audio/define.mp3")
            playing = True
            play(song)
            playing = False
            dictionary_result = None
            time.sleep(2)

            song = AudioSegment.from_wav("audio/info.wav")
            playing = True
            play(song)
            playing = False
            first_second = datetime.datetime.now().second

            while True:
                second_time = datetime.datetime.now().second

                if answer is not None:
                    if "yes" in answer or "yeah" in answer or "sure" in answer or "of course" in answer:
                        while True:
                            if wikipedia_result == True and wikipedia_displayed == False:
                                song = AudioSegment.from_mp3("audio/wikipedia.mp3")
                                playing = True
                                play(song)
                                playing = False
                                wikipedia_result = None

                                time.sleep(2)

                                song = AudioSegment.from_wav("audio/info.wav")
                                playing = True
                                play(song)
                                playing = False
                                first_second = datetime.datetime.now().second

                                while True:
                                    second_time = datetime.datetime.now().second

                                    if answer is not None:
                                        if "yes" in answer or "yeah" in answer or "sure" in answer or "of course" in answer:
                                            while True:
                                                if google_result == True and google_displayed == False:
                                                    song = AudioSegment.from_mp3(
                                                        "audio/google.mp3")
                                                    playing = True
                                                    play(song)
                                                    playing = False
                                                    google_result = None
                                                    break
                                        elif "no" in answer or "nope" in answer or "never" in answer or "na" in answer:
                                            answer = None
                                            break

                                        else:
                                            break

                                    else:
                                        if (second_time - first_second) > 10:
                                            song = AudioSegment.from_wav(
                                                "audio/info.wav")
                                            playing = True
                                            play(song)
                                            playing = False

                            elif google_result == True and wikipedia_displayed == False:
                                song = AudioSegment.from_mp3("audio/google.mp3")
                                playing = True
                                play(song)
                                playing = False
                                break

                    elif "no" in answer or "nope" in answer or "never" in answer or "na" in answer:
                        answer = None
                        break

                    elif (second_time - first_second) > 10:
                        song = AudioSegment.from_wav("audio/info.wav")
                        playing = True
                        play(song)
                        playing = False
                        first_second = datetime.datetime.now().second
                else:
                    if (second_time - first_second) > 10:
                        song = AudioSegment.from_wav("audio/info.wav")
                        playing = True
                        play(song)
                        playing = False
                        first_second = datetime.datetime.now().second

        elif dictionary_result == False:
            while True:
                            if wikipedia_result == True and wikipedia_displayed == False:
                                song = AudioSegment.from_mp3("audio/wikipedia.mp3")
                                playing = True
                                play(song)
                                playing = False
                                wikipedia_result = None

                                time.sleep(2)

                                song = AudioSegment.from_wav("audio/info.wav")
                                playing = True
                                play(song)
                                playing = False
                                first_second = datetime.datetime.now().second

                                while True:
                                    second_time = datetime.datetime.now().second

                                    if answer is not None:
                                        if "yes" in answer or "yeah" in answer or "sure" in answer or "of course" in answer:
                                            while True:
                                                if google_result == True and google_displayed == False:
                                                    song = AudioSegment.from_mp3(
                                                        "audio/google.mp3")
                                                    playing = True
                                                    play(song)
                                                    playing = False
                                                    google_result = None
                                                    break
                                        elif "no" in answer or "nope" in answer or "never" in answer or "na" in answer:
                                            answer = None
                                            break
                                        else:
                                            break

                                    else:
                                        if (second_time - first_second) > 10:
                                            song = AudioSegment.from_wav(
                                                "audio/info.wav")
                                            playing = True
                                            play(song)
                                            playing = False
            

        in_thinking_process = False