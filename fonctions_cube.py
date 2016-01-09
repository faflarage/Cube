# -----------------------------------------------------------------
# fonctions_cube.py
# January,07 2016
# Cube's functions used by Cerveau_cube.py
# This file is used both with the desktop and Raspberry Pi versions 
# -----------------------------------------------------------------

import aiml
import duckduckgo
import os
import random
import serial
import smtplib
import subprocess
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Lists differences between the desktop and raspberry pi versions (mine is /home/pi/Cube/ for the Raspberry Pi...)
systeme = os.uname()
if systeme[1] == "raspberrypi" :
    player = "omxplayer "
    port_serie = '/dev/ttyAMA0'
    repertoire_sons = "/home/pi/Cube/Sons/"
    repertoire_aiml = "/home/pi/Cube/"
    
    # Initialisation of the pi camera with a 320 x 240 resolution
    import picamera
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
else :
    player = "mpg123 "
    port_serie = '/dev/ttyACM0'
    repertoire_sons = "/home/fab/Cube nouveau/Sons/"
    repertoire_aiml = "/home/fab/Cube nouveau/"
    
# Create a dictionnary for the sound files
dico_dossiers = {}
for dossier in os.listdir(repertoire_sons) :
    dico_dossiers[dossier] = os.listdir(repertoire_sons + dossier)
    
# Search for AIML files
liste_fichiers_aiml = os.listdir(repertoire_aiml + "Fichiers AIML/")

# Create automatically "Cube-AIML.xml" with the files in the "Fichiers AIML" folder
file = open(repertoire_aiml + "Cube-AIML.xml", 'w')
file.write("<aiml version='1.0'>\n\n")
file.write("<category>\n<pattern>LOAD CUBE AIML FILES</pattern>\n<template>\n\n")
for fichier in liste_fichiers_aiml :
    file.write("<learn>" + repertoire_aiml + "Fichiers AIML/" + fichier + "</learn>\n")
file.write("\n</template>\n</category>\n\n</aiml>")
file.close()

# AIML initialisation
cube = aiml.Kernel()
cube.learn(repertoire_aiml + "Cube-AIML.xml")
cube.respond("LOAD CUBE AIML FILES")
cube.setBotPredicate('name', 'Cube')
cube.setBotPredicate('master', 'faf')

# Create a serial with Arduino
ser = serial.Serial(port_serie, 9600, timeout=1)
ser.flushInput()
ser.readline()

# Here is the core of Cube: these functions are used by Cerveau_cube.py to do what we want
def analyse(sentence):
    # Split the words and put them in a list
    liste_mots = sentence.split()
    print liste_mots, len(liste_mots)
        
    if liste_mots[0] == "say" and len(liste_mots) > 1 :
        # Say the sentence and display some informations
        phrase = " ".join(liste_mots[1:])
        info = "An order was passed, function Say : " + phrase + "\n"
        print info
        dit(phrase)
        
    elif liste_mots[0] == "go" and len(liste_mots) > 1 :
        # Going in the given direction and display some informations
        if liste_mots[1] == "ahead" :
            # Go ahead until there's a barrier
            info = "An order was passed, function Go : ahead"
            print info
            type_capteur = avance()
        elif liste_mots[1] == "back" :
            # Go back (20 cm)
            info = "An order was passed, function Go : back"
            print info
            recule()
        elif liste_mots[1] == "away" :
            # Rolls with an avoidance algorithm
            info = "An order was passed, function Go : away"
            print info
            for i in range(3) :
                type_capteur = avance()
                if type_capteur == 0 :
                    info = "Right switch activated -> left rotation"
                    print info
                    rotation_gauche(2)
                elif type_capteur == 1 :
                    info = "Left switch activated -> right rotation"
                    print info
                    rotation_droite(2)
                else :
                    distance_US = ping()
                    dist = str(distance_US[0]) + ", " + str(distance_US[1]) + ", " + str(distance_US[2])
                    info = "Ping made from left to right : " + dist + "\n"
                    if distance_US[0] > distance_US[2] :
                        info = info + "Left ping greater -> left rotation"
                        print info
                        rotation_gauche(2)
                    else :
                        info = info + "Right ping greater -> right rotation"
                        print info
                        rotation_droite(2)
    
    elif liste_mots[0] == "move" :
        # Go ahead until we ask Cube to stop
        info = "Move forward"
        print info
        move()
        
    elif liste_mots[0] == "stop" :
        # Stop Cube s wheels
        info = "Stop Cube"
        print info
        stop()
        
    elif liste_mots[0] == "turn" and len(liste_mots) > 1 :
        # Turn and display some informations
        if liste_mots[1] == "left" :
            info = "An order was passed, function Turn : left"
            print info
            rotation_gauche(1)
        elif liste_mots[1] == "right" :
            info = "An order was passed, function Turn : right"
            print info
            rotation_droite(1)
            
    elif liste_mots[0] == "ping" :
        # Ultrasonic wave and display some informations
        distance_US = ping()
        print distance_US
        dist = str(distance_US[0]) + ", " + str(distance_US[1]) + ", " + str(distance_US[2])
        info = "An order was passed, function Ping\n"
        info = info + "From left to right : " + dist + "\n"
        print info
        
    elif liste_mots[0] == "ir" :
        # Infrared wave and display some informations
        distance_IR = infrarouge()
        print distance_IR
        dist = str(distance_IR[0]) + ", " + str(distance_IR[1]) + ", " + str(distance_IR[2])
        info = "An order was passed, function InfraRed\n"
        info = info + "From left to right : " + dist + "\n"
        print info
        
    elif liste_mots[0] == "melodie" :
        # Play a melody and display some informations
        info = "An order was passed, function Melody\n"
        print info
        melodie()
        
    elif liste_mots[0] == "off" :
        # Shutdown the Pi and display some informations
        info = "The END of the program has been ordered, goodbye and see you soon !\n"
        print info
        dit("this the end")
        os.system('sudo halt')
        
    elif liste_mots[0] == "play" and len(liste_mots) > 1 :
        # Play a .mp3 file
        for dossier in dico_dossiers.keys() :
            for fichier_son in dico_dossiers[dossier] :
                if liste_mots[1] in fichier_son.lower() :
                    chemin_mp3 = repertoire_sons + dossier + '/' + fichier_son
                    info = "An order was passed, function Play : " + fichier_son + "\n"
                    print info
                    joue(chemin_mp3)
                    break
        
    elif liste_mots[0] == "email" :
        # Send an email
        send_email("fherve1974@gmail.com", "Salut", "Test de fonctionnement de la fonction email du Cube...")
    
    elif liste_mots[0] == "take" and "picture" in liste_mots :
        # Take a picture
        take_picture()
    
    else :
        # There's no known order, so the question is submitted to the AIML analyser
        reponse = cube.respond(sentence)
        info = "No known order : " + sentence + "\n"
        info = info + "After an AIML analysis, the response is : " + reponse +"\n"
        print info
        # Say the response or play a .mp3 file
        if reponse == "insult" :
            # Insult the user
            nb_sons = len(dico_dossiers["insulte"])
            fichier = dico_dossiers["insulte"][random.randrange(0,nb_sons,1)]
            joue(repertoire_sons + "insulte/" + fichier)
        elif reponse[:6] == "search" :
            # Search for a response on the net because the answer isn't in the AIML database
            source = ""
            search_words = reponse[7:]
            recherche = search_on_net(search_words)
            if recherche[:4] == "http" :
                recherche = "Sorry, I dont't know"
            elif "duckduckgo" in recherche :
                source = "Info from DuckDuckGo :"
                start = recherche.find(search_words[0].upper()) + len(search_words)
                end = recherche.find('.')
                recherche = recherche[start:end]
            elif "wikipedia" in recherche :
                source = "Info from Wikipedia :"
                end = recherche.find('.')
                recherche = recherche[:end]
            print source, recherche
            dit(recherche)
        elif reponse[:19] == "OK, now I know that" :
            dit(reponse)
            reponse = reponse[20:].split()
            verb_list = ["is", "was", "means", "is a", "are", "has"]
            for a in verb_list :
                if a in reponse :
                    verb = a
                    offset = reponse.index(verb)
                    pos1 = " ".join(reponse[:offset])
                    pos2 = " ".join(reponse[offset + 1:])
                    if verb == "means" :
                        pattern = "does " + pos1 + " means " + pos2
                    else :
                        pattern = verb + " " + pos1 + " " + pos2
                    pattern = pattern.upper()
                    print pattern
            
            text = "<category>\n  <pattern>" + pattern + "</pattern>\n  "
            text = text + "<template>" + "Yes, " + pos1 + " " + verb + " " + pos2 + "</template>\n</category>\n\n"
            print text
            modify_aiml_learned_file(text)
            cube.learn(repertoire_aiml + "Fichiers AIML/learned.aiml")
            
        else :
            dit(reponse)

def avance():
    # Go forward until there s a barrier
    ser.write("forward")
    # Wait for the end of the movement
    time.sleep(0.1)
    while 1:
        reponse = ser.readline()
        if reponse <> "" :
            break
    type_capteur = int(reponse)
    reponse = ""
    return type_capteur

def dit(phrase):
    # Say a sentence thanks to the espeak program (must be installed through apt-get)
    synthvoc = 'espeak -a200 -w out.wav "' + phrase + '" && aplay out.wav'
    subprocess.call(synthvoc, shell=True)

def infrarouge():
    # Infrared measures
    ser.flushInput()
    ser.readline()
    ser.write("ir")  
    # Wait for the end of the measures
    time.sleep(0.2)
    while 1:
        reponse = ser.readline()
        if reponse <> "" :
            break
    distance_IR = reponse.split()
    reponse = ""
    # Send IR values to Cerveau_cube.py
    try:
        for n in range(3) :
            distance_IR[n] = int(distance_IR[n])
    except:
        distance_IR = [0, 0, 0]
    return distance_IR

def joue(mp3):
    # Play a .mp3 file. Player is omxplayer for the Raspberry Pi, else mpg123
    fichier = player + '"' + mp3 + '" 2>/dev/null'
    subprocess.call(fichier, shell=True)
    
def lecture_arduino():
    # Read the datas from the Arduino
    ser.flushInput()
    reponse = ser.readline()
    reponse = reponse.lower()
    return reponse

def melodie():
    # Play a melody
    ser.write("melodie")

def modify_aiml_learned_file(text):
    # Modify learned.aiml file in order to add what Cube has learned
    file = open(repertoire_aiml + "Fichiers AIML/learned.aiml", 'r')
    contenu = file.read()
    file.close()
    contenu = contenu[73:-9] + "\n"
    contenu = contenu + text
    file = open(repertoire_aiml + "Fichiers AIML/learned.aiml", 'w')
    file.write('<?xml version="1.0" encoding="ISO-8859-15"?>\n\n<aiml>\n<!--author: Cube-->\n')
    file.write(contenu)
    file.write("\n</aiml>")
    file.close()

def move():
    # Go forward
    ser.write("move")

def ping():
    # Ultrasonic measures
    ser.flushInput()
    ser.readline()
    ser.write("ping")
    # Wait for the end of the measures
    time.sleep(0.1)
    while 1:
        reponse = ser.readline()
        if reponse <> "" :
            break
    distance_US = reponse.split()
    reponse = ""
    # Send distances to Cerveau_cube.py
    try:
        for n in range(3) :
            distance_US[n] = int(distance_US[n])
    except:
        distance_US = [0, 0, 0]
    return distance_US

def recule():
    # Go back
    ser.write("backward")
    
def rotation_droite(multiple):
    # Right rotation
    ser.write("turnr")
    # Wait for the end of the movement
    time.sleep(0.5)
    while 1:
        reponse = ser.readline()
        if reponse <> "" :
            reponse = ""
            break

def rotation_gauche(multiple):
    # Left rotation
    ser.write("turnl")
    # Wait for the end of the movement
    time.sleep(0.5)
    while 1:
        reponse = ser.readline()
        if reponse <> "" :
            reponse = ""
            break
    
def search_on_net(data):
    # Search for a response to the question thanks to the DuckDuckGo API
    try:
        response = duckduckgo.get_zci(data)
    except:
        response = "Sorry, I dont't know"
    return response

def send_email(recipient, subject, text):
    # Send an email, enter here your own parameters: gmail_user = mail adress of your robot and gmail_pwd = your password
    gmail_user = "*"
    gmail_pwd = "*"
    
    # Create the email message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = "Cube"
    msg['To'] = recipient
    # Create the text
    text = MIMEText(text)
    msg.attach(text)
    # Then, include an image with the text, if needed
    img_data = open(repertoire_aiml + "photo.jpg", 'rb').read()
    img = MIMEImage(img_data)
    msg.attach(img)
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(gmail_user, recipient, msg.as_string())
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"
        
def stop():
    # Stop the wheels
    ser.write("stop")

def take_picture():
    # Take a picture with the cam if we are working with the Raspberry Pi
    if systeme[1] == "raspberrypi" :
        camera.capture(repertoire_aiml + 'photo.jpg')
    else :
        pass
    