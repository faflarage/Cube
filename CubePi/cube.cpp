/*****************************************************************************************************************************************/
/*                                                                                                                                       */
/*                                        cube.cpp, Implémentation des commandes (Source File)                                           */
/*                                                                                                                                       */
/*****************************************************************************************************************************************/

#include "cube.h"

// Configuration du gyroscope (MPU6050) ___________________________________________________________________________________________________

#include "I2Cdev.h"
#include "MPU6050.h"

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

MPU6050 accelgyro;

int16_t gx, gy, gz;

// Déclaration des broches de l'Arduino utilisées__________________________________________________________________________________________

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

// Affichage LCD
const byte RS = 8;
const byte E = 9;
const byte D4 = 10;
const byte D5 = 11;
const byte D6 = 12;
const byte D7 = 13;

// Mélodies : nom des notes (C = DO, etc...) et leurs fréquences___________________________________________________________________________

char nomNotes[] = {'C','D','E','F','G','a','b'};
unsigned int frequences[] = {262,294,330,349,392,440,494};


/*****************************************************************************************************************************************/
/*                                                                                                                                       */
/*                                              Déclaration des fonctions du Cube                                                        */
/*                                                                                                                                       */
/*****************************************************************************************************************************************/

void initialisation() //_______________________________________________________ Fonctions d'initialisations
{
  // Initialisation du LCD
  LiquidCrystal lcd(RS,E,D4,D5,D6,D7);
  // Ecran utilise de 16 caracteres sur 2 lignes
  lcd.begin(16,2);
  // Affiche Hello
  lcd.print("Hello");

  // Rejoint le bus I2C puis initialise le gyroscope
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
      Wire.begin();
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
      Fastwire::setup(400, true);
  #endif
  
  accelgyro.initialize();
}

int envoiIR(byte capteurIR) //_______________________________________________________________ Envoi infrarouge
{
  // Envoi infrarouge avec le capteur concerné
  float distance = 0;
  float cumulDistance = 0;

  // 3 mesures sont effectuees puis sont moyennees pour diminuer le risque d erreur de mesure
  for (byte i = 0; i < 3; i++)
  {
    distance = analogRead(capteurIR);
    delay(10);
    cumulDistance += distance;
  }
  int valeurMoyIR = (int)(cumulDistance / 3);

  return(valeurMoyIR);
}

long envoiUS(byte capteurUStrig, byte capteurUSecho) //_______________________________________________________________ Envoi ultrasons
{
  // Effectue un ping avec le capteur US concerné
  long distance[5];
  long temp;
  
  // 3 mesures sont effectuees puis sont moyennees pour diminuer le risque d erreur de mesure
  for (int i=0; i<5; i++)
  {
    digitalWrite(capteurUStrig, LOW);
    delayMicroseconds(2);
    digitalWrite(capteurUStrig, HIGH);
    delayMicroseconds(10);
    digitalWrite(capteurUStrig, LOW);

    temp = pulseIn(capteurUSecho, HIGH, 25000);
    distance[i] = temp / 58; // Conversion de la mesure en cm
    delay(50);
  }
  
  temp = (distance[1] + distance[2] + distance[3]) / 3;
  return(temp);
}

byte avance() //________________________________________________________________ Va en avant jusqu a la rencontre d obstacle
{
  long temps = 0;                    // Temps nécessaire au calcul de la distance parcourue
  byte valeurG = 0;                  // Recueil l'état des capteurs de contact
  byte valeurD = 0;
  int distanceIRgauche = 0;          // Recueil des capteurs infrarouges
  int distanceIRcentre = 0;
  int distanceIRdroite = 0;
  long distanceUScentre = 0;         // Recueil du capteur ultrason central
  byte typeCapteur = 0;              // Recueil le type de capteur actionne quand un obstacle est rencontre
  
  // Vitesse maximale des moteurs = 255
  analogWrite(enablePinGauche, 255);
  analogWrite(enablePinDroit, 255);

  // Roues gauche et droite pour un deplacement en avant
  digitalWrite(in1PinGauche, HIGH); 
  digitalWrite(in2PinGauche, LOW);

  digitalWrite(in1PinDroit, HIGH); 
  digitalWrite(in2PinDroit, LOW);
  
  temps = millis();  // Temps de départ
  
  while(true)
  {
    // Recueille l'état des capteurs ultrason central, infrarouges et de contacts
    distanceUScentre = envoiUS(capteurUScentralTrig, capteurUScentralEcho);
    
    distanceIRgauche = envoiIR(capteurIRgauche);
    distanceIRcentre = envoiIR(capteurIRcentral);
    distanceIRdroite = envoiIR(capteurIRdroit);
    
    valeurG = digitalRead(capteurContactG);
    valeurD = digitalRead(capteurContactD);
    
    // Routine de detection d obstacle par les differents capteurs
    if (valeurG == HIGH) { typeCapteur = 0; break; }
    else if (valeurD == HIGH) { typeCapteur = 1; break; }
    else if ((distanceIRgauche > 460) || (distanceIRcentre > 460) || (distanceIRdroite > 460)) { typeCapteur = 2; break; }
    else if (distanceUScentre < 20) { typeCapteur = 3; break; }
  }
  
  stop();
  temps = ((millis() - temps) * 13) / 1000;         // Temps parcouru en secondes converti en cm (vitesse de 13 cm/s)
  
  // Si un capteur de contact est declenche le robot recule de 20 cm, de 10 cm si c est un capteur infrarouge et ne recule pas si c est le capteur ultrason
  if ((typeCapteur == 0) || (typeCapteur == 1)) { recule(20); }
  else if (typeCapteur == 2) { recule(10); }
  else if (typeCapteur == 3) { ; }
  
  return(typeCapteur);
}

void move() //________________________________________________________________ Va en avant
{
  // Vitesse maximale des moteurs = 255
  analogWrite(enablePinGauche, 255);
  analogWrite(enablePinDroit, 255);

  // Roues gauche et droite pour un deplacement en avant
  digitalWrite(in1PinGauche, HIGH); 
  digitalWrite(in2PinGauche, LOW);

  digitalWrite(in1PinDroit, HIGH); 
  digitalWrite(in2PinDroit, LOW);
}

void recule(int recul) //________________________________________________________________ Va en arrière de (recul) cm
{
  // Vitesse maximale des moteurs = 255
  analogWrite(enablePinGauche, 255);
  analogWrite(enablePinDroit, 255);

  // Roues gauche et droite pour un deplacement en arriere
  digitalWrite(in1PinGauche, LOW); 
  digitalWrite(in2PinGauche, HIGH);

  digitalWrite(in1PinDroit, LOW); 
  digitalWrite(in2PinDroit, HIGH);
  
  recul = (recul * 1000) / 13;  // Conversion distance - temps
  delay(recul);  // Correspond au temps de recul transmis
  
  stop();
}

void stop() //________________________________________________________________ Stoppe les moteurs
{
  digitalWrite(in1PinGauche, LOW); 
  digitalWrite(in2PinGauche, LOW);

  digitalWrite(in1PinDroit, LOW); 
  digitalWrite(in2PinDroit, LOW);
}

void tourneDroite(int angulation)
{
  // Vitesse maximale des moteurs = 255
  analogWrite(enablePinGauche, 255);
  analogWrite(enablePinDroit, 255);

  // Rotation des roues en sens inverse pour une rotation a droite de l'angle (angulation)
  digitalWrite(in1PinGauche, HIGH); 
  digitalWrite(in2PinGauche, LOW);

  digitalWrite(in1PinDroit, LOW);
  digitalWrite(in2PinDroit, HIGH);

  float zdps;
  float angle;
  
  // Tourne tant que l angle desire n est pas atteint
  do
  {
    accelgyro.getRotation(&gx, &gy, &gz);
    zdps = gz / 131;
    angle += abs(zdps) * 0.01;
    delay(8);
  } 
  while (angle < angulation);
  angle = 0;

  // Les 2 roues sont immobiles
  stop();
}

void tourneGauche(int angulation)
{
  // Vitesse maximale des moteurs = 255
  analogWrite(enablePinGauche, 255);
  analogWrite(enablePinDroit, 255);

  // Rotation des roues en sens inverse pour une rotation a gauche de l'angle (angulation)
  digitalWrite(in1PinGauche, LOW);
  digitalWrite(in2PinGauche, HIGH);

  digitalWrite(in1PinDroit, HIGH);
  digitalWrite(in2PinDroit, LOW);

  float zdps;
  float angle;
  
  // Tourne tant que l angle desire n est pas atteint
  do
  {
    accelgyro.getRotation(&gx, &gy, &gz);
    zdps = gz / 131;
    angle += abs(zdps) * 0.01;
    delay(8);
  } 
  while (angle < angulation);
  angle = 0;

  // Les 2 roues sont immobiles
  stop();
}

void melodie(char musique[], byte longueurMusique, int duree) //______ Joue une partition
{
  // Doivent etre transmis les notes, la longueur de la partition (nombre de notes transmises) et la duree de chaque note
  pinMode(piezzo, OUTPUT);
  for (int i = 0; i < longueurMusique; i++)
  {
    for (int j = 0; j < 7; j++)
    {
      if (nomNotes[j] == musique[i])
        // Joue la note concernee
        tone(piezzo, frequences[j], duree);
    }
    delay(duree);
  }
  pinMode(piezzo, INPUT);
}


