# Cube
Cube's files : a versatile robot with a Raspberry Pi (model B) and an Arduino (Mega 2560)

It's composed of : infrared sensors (3), ultrasonic sensors (3), microswitchs (2), DC motors (2), one LCD screen, a camera, a speaker, a piezzo, serial communications (2, one bluetooth between androïd phone and arduino and the other between PC and arduino) and a WIFI connexion to the web.

This repository contains two arduino files (one for a serial communication with a desktop PC for testing purpose named CubePC.ino and one for a serial communication with a raspberry pi for embedded applications named CubePi.ino), two python 2.7 files (a main file named Cerveau-cube.py and the functions module named fonctions-cube.py) and AIML files for communication with humans.

The arduino manages the communication between humans (thanks to an androïd phone) and PC, the collection of sensors. He's able to do some bips via a piezzo and to print some messages via the LCD screen.

The PC (with linux OS) manages the whoole logic, the analysis of the human language (in english, thanks to an AIML interface). He's able to speak (or play ".mp3" files with a speaker), to connect to the web and to collect images/vids via a camera.

Locomotion is ensured with two dc motors via a L293D and a MPU6050 for perfect rotations.

The power is supplied thanks to a 12V Pb battery and a 9V battery (only for the speaker).

I hope you'll enjoy this project,
faf
