/******************************************************************************************************************************************
*                                                                                                                                         *
*                                     CubePi.ino, Programmation de la carte Arduino Mega 2560 du cube                                     *
*                                     Objet : Détection d'obstacles / capteurs de contacts et infrarouges                                 *
*                                             Test nouveau protocole de communication                                                     *
*                                     Date : 08/08/2015                                                                                   *
*                                                                                                                                         *
******************************************************************************************************************************************/


/*XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  DONNEES GLOBALES  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX*/

// Inclusion des librairies-------------------------------------------------------
#include <Wire.h>
#include <LiquidCrystal.h>
#include "cube.h"

// Déclaration des broches de l'Arduino utilisées---------------------------------

// Infrarouges
const byte capteurIRgauche = 0;
const byte capteurIRcentral = 1;
const byte capteurIRdroit = 2;

// Ultrasons
const byte capteurUSgaucheTrig = 47;
const byte capteurUSgaucheEcho = 46;
const byte capteurUScentralTrig = 45;
const byte capteurUScentralEcho = 44;
const byte capteurUSdroitTrig = 43;
const byte capteurUSdroitEcho = 42;

// Microswitchs
const byte capteurContactG = 49;
const byte capteurContactD = 48;

// Bips
const byte piezzo = 51;

// Pont en H (L293D)
const byte enablePinGauche = 3;
const byte enablePinDroit = 2;
const byte in1PinGauche = 38;
const byte in2PinGauche = 39;
const byte in1PinDroit = 41;
const byte in2PinDroit = 40;

// Déclaration des constantes globales-------------------------------------------------------------
String chaine;          // Chaine pour le recueil des liaisons series
String distUS;          // Chaine cree pour envoyer les distances US
String distIR;          // Chaine cree pour envoyer les distances infrarouges

long distUSgauche = 0;        // Distance du capteur US gauche
long distUScentre = 0;        // Distance du capteur US central
long distUSdroite = 0;        // Distance du capteur US droit

int distIRgauche = 0;        // Distance du capteur IR gauche
int distIRcentre = 0;        // Distance du capteur IR central
int distIRdroite = 0;        // Distance du capteur IR droit

byte valG = 0;        // Etat des capteurs de contact, HIGH si obstacle
byte valD = 0;

byte typeCapteur = 0; // Type de capteur actionne quand un obstacle est rencontre


/*XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  INITIALISATION  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX*/

void setup()
{
  // Définit les modes d'entrée ou de sorties des différentes broches--------------

  // Broches du L293D
  pinMode(in1PinGauche, OUTPUT);
  pinMode(in2PinGauche, OUTPUT);
  pinMode(enablePinGauche, OUTPUT);
  pinMode(in1PinDroit, OUTPUT);
  pinMode(in2PinDroit, OUTPUT);
  pinMode(enablePinDroit, OUTPUT);

  // Initialisation des microswitchs
  pinMode(capteurContactG, INPUT);
  pinMode(capteurContactD, INPUT);

  // Initialisation des capteurs ultrasons
  pinMode(capteurUSgaucheTrig, OUTPUT);
  pinMode(capteurUSgaucheEcho, INPUT);
  pinMode(capteurUScentralTrig, OUTPUT);
  pinMode(capteurUScentralEcho, INPUT);
  pinMode(capteurUSdroitTrig, OUTPUT);
  pinMode(capteurUSdroitEcho, INPUT);

  // Bip du piezzo
  pinMode(piezzo, INPUT);

  initialisation();
  
  // Etablit une liaison série PC - Arduino
  Serial1.begin(9600);
  // Etablit une liaison série Arduino - Android
  Serial2.begin(9600);
}

/*XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  PROGRAMME  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX*/

void loop()
{
  // Lecture du tel Android-----------------------------------------------------------------------------
  while (Serial2.available() > 0)
  {
    chaine = Serial2.readStringUntil('\n');
    // Envoi du message a l'ordi
    Serial1.println(chaine);
    chaine = "";
  }

  // Lecture du PC--------------------------------------------------------------------------------------
  while (Serial1.available() >0)
  {
    chaine = Serial1.readStringUntil('\n');
    if (chaine == "forward")
    {
      // Va en avant
      typeCapteur = avance();
      Serial1.println(typeCapteur);
    }
    else if (chaine == "backward")
    {
      // Va en arriere
      recule(20);
    }
    else if (chaine == "turnr")
    {
      // Rotation droite
      tourneDroite(80);
      Serial1.println("ok");
    }
    else if (chaine == "turnl")
    {
      // Rotation gauche
      tourneGauche(80);
      Serial1.println("ok");
    }
    else if (chaine == "ping")
    {
      // Effectue un Ping gauche à droite et l'affiche
      distUSgauche = envoiUS(capteurUSgaucheTrig, capteurUSgaucheEcho);
      delay(10);
      distUScentre = envoiUS(capteurUScentralTrig, capteurUScentralEcho);
      delay(10);
      distUSdroite = envoiUS(capteurUSdroitTrig, capteurUSdroitEcho);
            
      distUS = String(distUSgauche) + " " + String(distUScentre) + " " + String(distUSdroite);
      Serial1.println(distUS);
    }
    else if (chaine == "ir")
    {
      // Effectue un envoi infrarouge de gauche à droite et l'affiche
      distIRgauche = envoiIR(capteurIRgauche);
      distIRcentre = envoiIR(capteurIRcentral);
      distIRdroite = envoiIR(capteurIRdroit);
            
      distIR = String(distIRgauche) + " " + String(distIRcentre) + " " + String(distIRdroite);
      Serial1.println(distIR);
    }
    else if (chaine == "melodie")
    {
      // Joue une mélodie
      melodie("CCGGaaGFFEEDDC ", 15, 300);
    }
    chaine == "";
  }
}