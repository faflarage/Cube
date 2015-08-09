# ----------------------------------------------------------------------------------------
# Cerveau_cube.py
# Modife le 08 aout 2015
# Cerveau de cube 
# ----------------------------------------------------------------------------------------

import fonctions_cube
import re
import os

# Repertorie les differences entre les versions PC et Pi
systeme = os.uname()
if systeme[1] == "raspberrypi" :
    repertoire_sons = "/home/pi/Cube/Sons/"
else :
    repertoire_sons = "/home/fab/Cube nouveau/Sons/"
liste_sons = os.listdir(repertoire_sons)

def analyse():
    if liste_mots[0] == "say" and len(liste_mots) > 1 :
        # Dit la phrase transmise
        fonctions_cube.dit(" ".join(liste_mots[1:]))
        
    elif liste_mots[0] == "go" and len(liste_mots) > 1 :
        # Va dans la direction donnee
        if liste_mots[1] == "ahead" :
            # Va tout droit jusqu'a la detection d'un obstacle
            type_capteur = fonctions_cube.avance()
        elif liste_mots[1] == "back" :
            # Recule d'une vingtaine de cm
            fonctions_cube.recule()
        elif liste_mots[1] == "away" :
            # Se promene avec un algorithme d'evitement d'obstacles
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
        # Tourne
        if liste_mots[1] == "left" :
            fonctions_cube.rotation_gauche(1)
        elif liste_mots[1] == "right" :
            fonctions_cube.rotation_droite(1)
            
    elif liste_mots[0] == "ping" :
        # Effectue un envoi ultrason
        distance_US = fonctions_cube.ping()
        print distance_US
        
    elif liste_mots[0] == "ir" :
        # Effectue un envoi infrarouge
        distance_IR = fonctions_cube.infrarouge()
        print distance_IR      
    
    elif liste_mots[0] == "melodie" :
        # Joue une melodie
        fonctions_cube.melodie()
        
    elif liste_mots[0] == "off" :
        # Fermeture logicielle du Pi
        fonctions_cube.dit("this the end")
        os.system('sudo halt')
        
    elif liste_mots[0] == "play" and len(liste_mots) > 1 :
        # Joue le fichier son transmis
        for fichier in liste_sons :
            if liste_mots[1] in fichier.lower() :
                fonctions_cube.joue(repertoire_sons + fichier)
                break
    
    else :
        pass

fonctions_cube.joue(repertoire_sons + "Allumage_Cube.mp3")
fonctions_cube.dit("Hello I'm ready")

while 1:
    # Lecture du message envoye par l'utilisateur via le tel android
    reponse = fonctions_cube.lecture_arduino()
    
    if reponse <> "" :
        # Enleve les caracteres indesirables
        reponse = re.sub(r'[.!?]', "", reponse)
        # Separe les differents mots en les mettant dans une liste
        liste_mots = reponse.split()
        reponse = ""
        print liste_mots, len(liste_mots)
        
        # Analyse de la reponse
        analyse()
        