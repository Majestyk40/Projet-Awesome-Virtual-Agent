import os
import sys
import datetime
import pyttsx3
import speech_recognition as sr
import wikipedia
import wolframalpha
import webbrowser
import smtplib
import random
import requests

import pandas as pd

# Initialisation de la voix via Pyttsx3
engine = pyttsx3.init()
client = wolframalpha.Client('Rentrez ici vos ID')

# Paramétrage de la voix
# 0 est le code pour la voix française
voices = engine.getProperty('voices')[0]
engine.setProperty('voice', voices.id)

# Mise en place de la fonction talk
def avaSays(audio):
    print('AVA : ' + audio)
    engine.say(audio)
    engine.runAndWait()

# Mise en place de la fonction d'écoute de commandes de l'utilisateur
def userCommand():
    a = sr.Recognizer()
    with sr.Microphone() as sourceAudio:
        print("AVA : Je vous écoute...")
        a.pause_threshold = 1
        audio = a.listen(sourceAudio)
        try:
            command = a.recognize_google(audio, language='fr-FR')
            command = command.lower()
            print(command)           
        except sr.UnknownValueError:
            avaSays("Désolé je n'ai pas compris")
            print("Désolé je n'ai pas compris")
            command = userCommand();
        return command

def assistant(command):
    
    # Salutations suivant l'heure de la journée à l'ouverture du programme
    if 'salut' in command:
        CurrentHour = int(datetime.datetime.now().hour)
        if CurrentHour >= 6 and CurrentHour < 18:
            avaSays('Bonjour !')
        elif CurrentHour >= 18 and CurrentHour != 6:
            avaSays('Bonsoir !')
    
    #Présentation AVA
    if 'ava qui es tu' in command:
        avaSays('Je suis ava, un assistant virtuel autonome créé par Monsieur kadri')
    # Telecommande freebox
    # code= Correspond à votre code télécommande freebox, remplaçez les XXX par votre code
    elif 'coupe le son' in command:
        remote = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=mute')
    elif 'remets le son' in command:
        remote = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=mute')
    elif 'monte le son' in command:
        remote = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=vol_inc')
    elif 'baisse le son' in command:
        remote = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=vol_dec')
    elif 'mets tf1' in command:
        channel = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=1')
        avaSays('voici tf1')
    elif 'mets la 2' in command:
        channel = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=2')
        avaSays('voici france 2')
    elif 'mets la 3' in command:
        channel = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=3')
        avaSays('voici france 3')
    elif 'mets canal +' in command:
        channel = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=4')
        avaSays('voici canal +') 
    elif 'mets la 5' in command:
        channel = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=5')
        avaSays('voici france 5')
    elif 'mets m6' in command:
        channel = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=6')
        avaSays('voici m 6') 
    elif 'mets arté' in command:
        channel = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=7')
        avaSays('voici arté') 
    elif 'mets c8' in command:
        channel = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=8')
        avaSays('voici c8') 
    elif 'mets w9' in command:
        channel = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=9')
        avaSays('voici w 9') 
    elif 'mets tmc' in command:
        channelA = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=1')
        channel = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=0')
        avaSays('voici tmc')    
    elif 'mets tfx' in command:
        channelA = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=1')
        channel = requests.get('http://hd1.freebox.fr/pub/remote_control?code=XXXXXXXX&key=1')
        avaSays('voici tfx')    

    # Diverses conversations
    elif 'heure' in command:
        H = pd.datetime.now().hour
        Mn = pd.datetime.now().minute
        heure = str(H) + ' heures et ' + str(Mn) + ' minutes'
        avaSays('il est ' + heure)
    
    # Ouverture de Google
    elif 'google' in command:
        webbrowser.open('www.google.com')
        avaSays('google est prêt')
        
    # Module Météo
    elif 'météo' in command:
        apiUrl='http://api.openweathermap.org/data/2.5/weather?q='NOM DE VOTRE VILLE'&appid='VOTRE CLE API'&units=metric&lang=fr'
        meteo = requests.get(apiUrl)
        dataMeteo = meteo.json()
        temp=dataMeteo['main']['temp']
        temps = dataMeteo['weather'][0]['description']
        avaSays('il fait {} degrés'.format(temp))
        avaSays(temps)
        
    # Fermeture du programme        
    elif 'stop' in command:
        avaSays("A bientôt")
        sys.exit()

while True:
    assistant(userCommand())
