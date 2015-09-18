/*****************************************************************************************************************************************/
/*                                                                                                                                       */
/*                                          cube.h, Déclaration des commandes (Header File)                                              */
/*                                                                                                                                       */
/*****************************************************************************************************************************************/

// Evite que la librairie soit incluse plusieurs fois
#ifndef cube_h
#define cube_h

#include <Wire.h>
#include <LiquidCrystal.h>

// Inclus les définitions et constantes du language Arduino
#include "Arduino.h"

// Déclaration des fonctions

// Initialisation
void initialisation();							// Initialisation (LCD et gyroscope (MPU6050))

// Capteurs de distance
int envoiIR(byte capteurIR);						// Fonction infrarouge
long envoiUS(byte capteurUStrig, byte capteurUSecho);			// Fonction ultrason

// Mouvements
byte avance();
void recule(int recul);
void stop();
void tourneDroite(int angulation);
void tourneGauche(int angulation);

//Sons
void melodie(char musique[], byte longueurMusique, int duree);		// Joue une partition

#endif
