# ----------------------------------------------------------------------------------------
# Cerveau_cube.py
# September,18 2015
# Cube's brain
# This file is used both with the desktop and Raspberry Pi versions 
# ----------------------------------------------------------------------------------------

import fonctions_cube
import re
import os
import aiml

# Lists differences between the desktop and raspberry pi versions
# Be carefull with directories (mine is /home/pi/Cube/ for the Raspberry Pi...)
systeme = os.uname()
if systeme[1] == "raspberrypi" :
    repertoire_sons = "/home/pi/Cube/Sons/"
    repertoire_aiml = "/home/pi/Cube/"
else :
    repertoire_sons = "/home/fab/Cube nouveau/Sons/"
    repertoire_aiml = "/home/fab/Cube nouveau/"
liste_sons = os.listdir(repertoire_sons)
liste_fichiers_aiml = os.listdir(repertoire_aiml + "Fichiers AIML/")

def analyse():
    if liste_mots[0] == "say" and len(liste_mots) > 1 :
        # Say the sentence
        fonctions_cube.dit(" ".join(liste_mots[1:]))
        
    elif liste_mots[0] == "go" and len(liste_mots) > 1 :
        # Going in the given direction
        if liste_mots[1] == "ahead" :
            # Go ahead until there's a barrier
            type_capteur = fonctions_cube.avance()
        elif liste_mots[1] == "back" :
            # Go back (20 cm)
            fonctions_cube.recule()
        elif liste_mots[1] == "away" :
            # Rolls with an avoidance algorithm
            for i in range(3) :
                type_capteur = fonctions_cube.avance()
                print type_capteur
                if type_capteur == 0 :
                    print "capteur de contact droit active -> rotation gauche"
                    fonctions_cube.rotation_gauche(2)
                elif type_capteur == 1 :
                    print "capteur de contact gauche active -> rotation droite"
                    fonctions_cube.rotation_droite(2)
                else :
                    print "realisation d'un PING"
                    distance_US = fonctions_cube.ping()
                    print distance_US
                    if distance_US[0] > distance_US[2] :
                        print "Mesure + grande a gauche -> rotation gauche"
                        fonctions_cube.rotation_gauche(2)
                    else :
                        print "Mesure + grande a droite -> rotation droite"
                        fonctions_cube.rotation_droite(2)
        
    elif liste_mots[0] == "turn" and len(liste_mots) > 1 :
        # Turn
        if liste_mots[1] == "left" :
            fonctions_cube.rotation_gauche(1)
        elif liste_mots[1] == "right" :
            fonctions_cube.rotation_droite(1)
            
    elif liste_mots[0] == "ping" :
        # Ultrasonic wave
        distance_US = fonctions_cube.ping()
        print distance_US
        
    elif liste_mots[0] == "ir" :
        # Infrared wave
        distance_IR = fonctions_cube.infrarouge()
        print distance_IR      
    
    elif liste_mots[0] == "melodie" :
        # Play a melody
        fonctions_cube.melodie()
        
    elif liste_mots[0] == "off" :
        # Shutdown the Pi
        fonctions_cube.dit("this the end")
        os.system('sudo halt')
        
    elif liste_mots[0] == "play" and len(liste_mots) > 1 :
        # Play a .mp3 file
        for fichier in liste_sons :
            if liste_mots[1] in fichier.lower() :
                fonctions_cube.joue(repertoire_sons + fichier)
                break
    
    else :
        reponse = cube.respond(question)
        print reponse
        # Say the response or play a .mp3 file
        fonctions_cube.dit(reponse)

fonctions_cube.joue(repertoire_sons + "Allumage_Cube.mp3")
fonctions_cube.dit("Hello I'm ready")

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

while 1:
    # Read the words of the user via the android phone
    question = fonctions_cube.lecture_arduino()
    
    if question <> "" :
        # Remove the unwanted characters
        question = re.sub(r'[.!?]', "", question)
        # Split the words and put them in a list
        liste_mots = question.split()
        print liste_mots, len(liste_mots)
        
        # Call for an analysis of the sentence
        analyse()
        