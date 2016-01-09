# ----------------------------------------------------------------------------------------
# Cerveau_cube.py
# January,07 2016
# Cube's brain
# This file is used both with the desktop and Raspberry Pi versions 
# ----------------------------------------------------------------------------------------

import fonctions_cube
import os
import random
import re
import time

# Lists differences between the desktop and raspberry pi versions
# Be carefull with directories (mine is /home/pi/Cube/ for the Raspberry Pi...)
systeme = os.uname()
if systeme[1] == "raspberrypi" :
    dir_sons = "/home/pi/Cube/Sons/"
    dir_aiml = "/home/pi/Cube/"
else :
    dir_sons = "/home/fab/Cube nouveau/Sons/"
    dir_aiml = "/home/fab/Cube nouveau/"
    
# Create a dictionnary for sound files
dict_directories = {}
for directory in os.listdir(dir_sons) :
    dict_directories[directory] = os.listdir(dir_sons + directory)

fonctions_cube.joue(dir_sons + "jingle/Allumage_Cube.mp3")
fonctions_cube.dit("Hello I'm ready")

# Base for time
t0 = time.time()

# Display some informations
info = "Welcome in Cube's interface\n"
info = info + "You're working on " + systeme[1] + "\n"
info = info + "Your working directory is : " + dir_aiml + "\n"
info = info + "Now, Cube is waiting for an order from you...\n"
print info
print dict_directories

while 1:
    # Play something if nothing happens
    t1 = time.time()
    if t1 - t0 > 30 :
        nb_sons = len(dict_directories["attente"])
        fichier = dict_directories["attente"][random.randrange(0,nb_sons,1)]
        fonctions_cube.joue(dir_sons + "attente/" + fichier)
        t0 = time.time()
    
    # Read the words of the user via the android phone
    question = fonctions_cube.lecture_arduino()
    if question <> "" :
        # Remove unwanted characters
        question = re.sub(r'[.!?]', "", question)
        # Test to look for AND or THEN in the sentence
        if "and" in question :
            liste_questions = question.split("and")
            # Call for an analysis of the sentences
            fonctions_cube.analyse(liste_questions[0])
            fonctions_cube.analyse(liste_questions[1])
        elif "then" in question :
            liste_questions = question.split("then")
            # Call for an analysis of the sentences
            fonctions_cube.analyse(liste_questions[0])
            fonctions_cube.analyse(liste_questions[1])
        else :        
            # Call for an analysis of the sentence
            fonctions_cube.analyse(question)
        t0 = time.time()
        