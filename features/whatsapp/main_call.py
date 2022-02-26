# basic imports
import pyautogui as jarvis
jarvis.FAILSAFE=False   # This is to avoid the program to close when the mouse is not found
import time
import pytesseract
import pyautogui
from PIL import ImageGrab
import os
import pygame

class _call_ ():
    initial_location=''
    import reply_engine

    # initiate the mixer
    global init_mixer
    def init_mixer():
        pygame.mixer.init(devicename='Jarvis - Speaker (VB-Audio Virtual Cable)')

    # initiate the pygame mixer once the program starts
    init_mixer()

    # text to speech engine
    global engine
    import pyttsx3
    engine = pyttsx3.init()     # initialise the engine
    voices = engine.getProperty('voices')   
    engine.setProperty('voice', voices[1].id)   # set the voice
    newVoiceRate = 135
    engine.setProperty('rate',newVoiceRate)    # set the speed rate

    # sleep function
    global sleep
    def sleep(sec):
        time.sleep(sec)

    # calculate len of wave file
    global calculate_wave_len
    def calculate_wave_len(wave_file=initial_location+'output.wav'):
        import wave
        wav = wave.open(wave_file, 'rb')
        frames = wav.getnframes()
        rate = wav.getframerate()
        duration = frames / float(rate)
        return float(duration.__round__(2))

    # speech to text
    def jarvis_voice_recognise():
        import speech_recognition as sr
        speech = sr.Recognizer()

        with sr.Microphone(device_index=3) as source:

            speech.adjust_for_ambient_noise(source, duration=0.5)       # Adjust for ambient noises
            speech.pause_threshold=1
            print("Listening to call..............")

            try:
                audio = speech.listen(source, timeout=3, phrase_time_limit=6)                # set timeout here
                text = speech.recognize_google(audio, language='en-US') # recognize speech using Google Speech Recognition
                return text
            
            except sr.WaitTimeoutError as err:
                print('Timeout Error')
                print(err)

            except:
                print("Seems like you are not speaking or i can not understand you")
                return "Seems like you are not speaking or i can not understand you"

    # just a function to check the microphone
    def Check_Microphone():
        # merhod 01
        import speech_recognition as sr
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

        # method 02
        import sounddevice as sd
        print (sd.query_devices())
        
    # text to speech
    def jarvis_speak(text):
        # engine.say(text)
        pygame.mixer.quit()
        while True:
            try:
                os.remove('output.wav')     # delete the previous file
                break
            except PermissionError:
                print('Retrying to delete the previous file')
                continue

        engine.save_to_file(text, 'output.wav')
        engine.runAndWait()

        if __name__=="__main__":
            # play the audio file
            try:
                init_mixer()
            except:
                print('Mixer not initiated')
            pygame.mixer.music.load('output.wav')
            pygame.mixer.music.play()
            sleep(calculate_wave_len()-1)

    # caller name
    def Caller_Name():
        while True:       
            attend_call_cordinates=pyautogui.locateCenterOnScreen('img\call_attend.png', confidence=0.7)
            if attend_call_cordinates!=None:
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #Reinstall Tesseract-OCR in this location 'C:\Program Files\Tesseract-OCR'
                cap = ImageGrab.grab(bbox =(1630, 85, 1910, 130))
                ocr = pytesseract.image_to_string(cap, lang ='eng')
                print('Caller Name : ',ocr)
                return ocr
            else:
                print('No incoming call....')
                sleep(3)

    # attend call
    def attend_call():
        global attend_call_cordinates
        attend_call_cordinates=jarvis.locateCenterOnScreen('img\call_attend.png', confidence=0.7)
        if attend_call_cordinates!=None:
            print('Attending Call....',attend_call_cordinates)
            x=attend_call_cordinates[0]
            y=attend_call_cordinates[1]
            jarvis.click(x, y)
            jarvis.sleep(1.5)
        else:
            print('Can not find call_attend button...')

    # decline call
    def decline_call():
        global decline_call_cordinates
        decline_call_cordinates=jarvis.locateCenterOnScreen('img\call_decline.png', confidence=0.7)
        if decline_call_cordinates!=None:
            print('Declining Call....',decline_call_cordinates)
            x=decline_call_cordinates[0]
            y=decline_call_cordinates[1]
            jarvis.click(x, y)
            jarvis.sleep(1)
        else:
            print('Can not find decline_attend button...')

    # cut call
    def cut_call():
        try:
            cut_call_cordinates=jarvis.locateCenterOnScreen('img\call_cut.png', confidence=0.7)
            if cut_call_cordinates!=None:
                print('Cutting Call....',cut_call_cordinates)
                x=cut_call_cordinates[0]
                y=cut_call_cordinates[1]
                jarvis.click(x, y)
                jarvis.sleep(1)
        except:
            print('Can not find cut call button...')

    # check if the call is in progress
    def check_call():
        call_in_progress=jarvis.locateCenterOnScreen('img\call_in_progress.png', confidence=0.7)
        if call_in_progress!=None:
            print('Call in progress........')
            return True
        else:
            print('No call in progress........')
            return False

    # check incoming call
    def check_incoming_call():
        attend_call_cordinates=jarvis.locateCenterOnScreen('img\call_attend.png', confidence=0.7)
        if attend_call_cordinates!=None:
            return True
        else:
            print('No incoming call....')
            sleep(3)
            return False

    # main function
    if __name__ == '__main__':
        while True:
            if check_incoming_call() == True:

                user = Caller_Name()    # get the caller name
                attend_call()        # attend the call
                
                if attend_call_cordinates!=None:
                    print('Call Attended........')
                    jarvis_speak('Hello ' + user + 'I am jarvis, AI bot. How can I help you?')

                    while True:
                        user_said = jarvis_voice_recognise()    # get the user input
                        print('User said : ',user_said)
                        reply = reply_engine.Reply_Engine(msg_input = user_said)   # get the reply
                        jarvis_speak(reply)

                        print('user has been answered........')
                        print('reply to user :',reply)

                        if reply == 'Good Bye Sir have a nice day' or check_call() == False:
                            cut_call()
                            break

'''
FUTURE WORKS:
    1. add a virtual microphone to the program      --> done
    2. integrate with main jarvis program       --> working
    3. if user cuts the call, then the program will not wait for the user to say anything      --> done
'''