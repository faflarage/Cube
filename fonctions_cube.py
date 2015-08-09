# -----------------------------------------------------------------
# fonctions_cube.py
# Modifie le 08 aout 2015
# Module creant les fonctions de cube
# -----------------------------------------------------------------

import serial
import subprocess
import time
import os

# Repertorie les differences entre les versions PC et Pi
systeme = os.uname()
if systeme[1] == "raspberrypi" :
    player = "omxplayer "
    port_serie = '/dev/ttyAMA0'
else :
    player = "mpg123 "
    port_serie = '/dev/ttyACM0'

# Cree la liaison serie avec l'Arduino
ser = serial.Serial(port_serie, 9600, timeout=1)

def avance():
    ser.write("forward")
    # Attend 100 ms puis recueille la distance parcourue
    time.sleep(0.1)
    while 1:
        reponse = ser.readline()
        if reponse <> "" :
            break
    type_capteur = int(reponse)
    reponse = ""
    return type_capteur
    
def recule():
    ser.write("backward")
    
def rotation_gauche(multiple):
    ser.write("turnl")
    # Attend 100 ms puis attend que la rotation soit effectuee
    time.sleep(0.5)
    while 1:
        reponse = ser.readline()
        if reponse <> "" :
            reponse = ""
            break
    
def rotation_droite(multiple):
    ser.write("turnr")
    # Attend 100 ms puis attend que la rotation soit effectuee
    time.sleep(0.5)
    while 1:
        reponse = ser.readline()
        if reponse <> "" :
            reponse = ""
            break
    
def ping():
    ser.write("ping")
    # Attend 100 ms puis cree une liste de recueil des distances US
    time.sleep(0.1)
    while 1:
        reponse = ser.readline()
        if reponse <> "" :
            break
    distance_US = reponse.split()
    reponse = ""
    for n in range(3) :
        distance_US[n] = int(distance_US[n])
    return distance_US
    
def infrarouge():
    ser.write("ir")  
    # Attend 100 ms puis cree une liste de recueil des distances infrarouges
    time.sleep(0.1) 
    reponse = ser.readline()
    distance_IR = reponse.split()
    for n in range(3) :
        distance_IR[n] = int(distance_IR[n])
    return distance_IR
    
def melodie():
    ser.write("melodie")
    
def dit(phrase):
    synthvoc = 'espeak -a200 "' + phrase + '" 2>/dev/null'
    subprocess.call(synthvoc, shell=True)
    
def lecture_arduino():
    # Lit les donnees envoyee par l'Arduino et les met en minuscules
    reponse = ser.readline()
    reponse = reponse.lower()
    return reponse

def joue(mp3):
    fichier = player + '"' + mp3 + '" 2>/dev/null'
    subprocess.call(fichier, shell=True)
    