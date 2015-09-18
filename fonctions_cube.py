# -----------------------------------------------------------------
# fonctions_cube.py
# September,18 2015
# Cube's functions used by Cerveau_cube.py
# This file is used both with the desktop and Raspberry Pi versions 
# -----------------------------------------------------------------

import serial
import subprocess
import time
import os

# Lists differences between the desktop and raspberry pi versions
systeme = os.uname()
if systeme[1] == "raspberrypi" :
    player = "omxplayer "
    port_serie = '/dev/ttyAMA0'
else :
    player = "mpg123 "
    port_serie = '/dev/ttyACM0'

# Create a serial with Arduino
ser = serial.Serial(port_serie, 9600, timeout=1)

def avance():
    # Go forward
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
    
def recule():
    # Go back
    ser.write("backward")
    
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
    
def ping():
    # Ultrasonic measures
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
    for n in range(3) :
        distance_US[n] = int(distance_US[n])
    return distance_US
    
def infrarouge():
    # Infrared measures
    ser.write("ir")  
    # Wait for the end of the measures
    time.sleep(0.1) 
    reponse = ser.readline()
    distance_IR = reponse.split()
    # Send values to Cerveau_cube.py
    for n in range(3) :
        distance_IR[n] = int(distance_IR[n])
    return distance_IR
    
def melodie():
    # Play a melody
    ser.write("melodie")
    
def dit(phrase):
    # Say a sentence thanks to the espeak program (must be installed through apt-get)
    synthvoc = 'espeak -a200 "' + phrase + '" 2>/dev/null'
    subprocess.call(synthvoc, shell=True)
    
def lecture_arduino():
    # Read the datas from the Arduino
    reponse = ser.readline()
    reponse = reponse.lower()
    return reponse

def joue(mp3):
    # Play a .mp3 file. Player is omxplayer for the Raspberry Pi, else mpg123
    fichier = player + '"' + mp3 + '" 2>/dev/null'
    subprocess.call(fichier, shell=True)
    