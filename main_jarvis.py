import time
import speech_recognition as sr
import multiprocessing as mp
import threading as th
import winsound as ws 
import pyautogui as jarvis

# hotword detection
import features.wake_word as wake_word
def hotword_detection():
    wake_word.wake_word_detection(music_file='features\chime.wav', model=['voice_model\jarvis_windows.ppn','voice_model\hey-jarvis_windows.ppn'])

# initialize the recognizer
speech = sr.Recognizer()

# initialize the engine
import pyttsx3
engine = pyttsx3.init()     # initialise the engine

voices = engine.getProperty('voices')   
engine.setProperty('voice', voices[1].id)   # set the voice

newVoiceRate = 140
engine.setProperty('rate',newVoiceRate)    # set the speed rate

# sleep function
def sleep(sec):
    time.sleep(sec)

# speech to text
def jarvis_voice_recognise(tout=None, ptlimit=None):
    with sr.Microphone(device_index=1) as source:

        speech.adjust_for_ambient_noise(source, duration=0.5)       # Adjust for ambient noises
        print("Listening........")
        audio = speech.listen(source, timeout=tout, phrase_time_limit=ptlimit)                

        try:
            text = speech.recognize_google(audio, language='en-US').lower()
            print("You said : {}".format(text))
            return text

        except:
            print("Could not understand what you said")
            return "Could not understand what you said".lower()


# text to speech
def jarvis_speak(text):
    print('Jarvis : ', text)
    engine.say(text)
    engine.runAndWait()

# background music
def background_music(signal):
    if signal == 'start':
        ws.PlaySound('music\IronMan_Theme_Song.wav', ws.SND_ASYNC | ws.SND_ALIAS)
        print('Background music started')

    elif signal == 'stop':
        ws.PlaySound(None, ws.SND_ASYNC)
        print('Background music stopped')
    
    return

# 1. main process
def main(text): 

    if 'jarvis' == text:
        jarvis_speak('Yes sir')

    elif 'hello' in text:
        jarvis_speak('Hello sir')

    elif 'how are you' in text:
        jarvis_speak('I am fine sir')

    elif 'what is your name' in text:
        jarvis_speak('My name is jarvis')

    elif 'what is your age' in text:
        jarvis_speak('My software is still in development mode')

    elif 'what is your job' in text:
        jarvis_speak('I am a virtual assistant')

    elif 'what is your favourite colour' in text:
        jarvis_speak('My favourite colour is blue')

    elif 'what is your favourite song' in text:
        jarvis_speak('My favourite song is Iron Man Songs')

    elif 'Could not understand what you said' in text:
        print('Could not understand what you said')
    
    # Features
    elif 'attend my call' or 'respond my call' in text:
        import features.whatsapp.main_call as call
        call.__main__()
    
    else:
        jarvis_speak('This is not programmed yet.')

# 2. check new incoming call process
def check_for_new_call():   
    attend_call_cordinates=jarvis.locateCenterOnScreen('features\whatsapp\img\call_attend.png', confidence=0.7)
    if attend_call_cordinates!=None:
        jarvis_speak('Sir There is a new call')    #features to be added -to ask user whether to pick it up or not by jarvis or by you
        sleep(1)
    elif attend_call_cordinates== None:  #multiprocessing required
        print('No new call')           
        sleep(5)


if __name__ == '__main__':
    background_music('start')
    jarvis_speak('welcome back sir , all systems are online')
    background_music('stop')

    while True:
        hotword_detection()
        # text = jarvis_voice_recognise(ptlimit=5)
        # main(text)
        

    # # ===== doing multithreading ===== #
    # main_thread = th.Thread(target=main)
    # call_check_thread = th.Thread(target=check_for_new_call)

    # # starting the threads
    # # main_thread.start()
    # call_check_thread.start()

    # # joining the threads
    # # main_thread.join()
    # call_check_thread.join()
