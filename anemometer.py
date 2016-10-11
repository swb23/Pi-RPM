#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 21.07.2016
@author: Sander
Listen Durchschnitt bilden und Lise anpassen
test 2
'''

# Importiert die benoetigten Bibliotekne
import RPi.GPIO as GPIO
import datetime as dt
import time
import MySQLdb
import sys
import threading

#Globale Variablen setzten
global aufloesung 
aufloesung=1 #legt die Messaufloesung in Sekunden fest
global aufloesungzm     #Dauer der Zeit, über die der gleitende Mittelwert gebildet wird
aufloesungzm=2
global anzahlsensoren
anzahlsensoren=2
global zws1  
zws1=[]
global zws2  
zws2=[]
global db


# Teilt der GPIO Bibliotek mit die GPIO references zu nutzen
GPIO.setmode(GPIO.BCM)

# Setzt Pin 27 und Pin 17 als Inut
GPIO.setup(27 , GPIO.IN)
GPIO.setup(17 , GPIO.IN)

class timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #self.rpm=rpm
        self.daemon=True
        self.start()
    def run(self):
        while True:
            time.sleep(aufloesung)
            turbinerpm=mittelwert1()
            windrpm=mittelwert2()
            print("Turbinenrpm: " + turbinerpm + "/ Windgeschwindigkeit: " + windrpm)
            speichern(turbinerpm, windrpm)


def signalerkennung1(channel): # Turbine
    global zws1
    t10=dt.datetime.now()
    zws1.append(t10) #fuegt den akutellen Timestamp dem Zwischenspeicher für die Timestamps hinzu
    
def signalerkennung2(channel): # Anemometer (wind)
    global zws2
    t20=dt.datetime.now()
    zws2.append(t20) #fuegt den akutellen Timestamp dem Zwischenspeicher für die Timestamps hinzu        
       
    # Ermittelt aus den Messdaten des Sensors einen Durchschnittswert für die Dauer der Aufloesung  
def mittelwert1():
    global zws1
    t1=dt.datetime.now()-dt.timedelta(0,aufloesungzm)
    while True:
        if len(zws1)==0:
            break   # Loescht alle Werte die aelter als die dauer der Aufloesung sind
        elif t1>=zws1[0]:
            del zws1[0]
        else:
            break
    n=len(zws1)
    if n>1:     # Berechnet den zeitlichen Abstand zwischen dem ersten und letztem Messwert und berechnet die Umdrehung pro Minute
        dauer=zws1[n-1]-zws1[0]
        rpm=int( (60/dt.timedelta.total_seconds(dauer))*(n/anzahlsensoren))
	       # rpm=int(dt.timedelta.total_seconds(dauer)*n)
    elif n==0:
         rpm=0
    else:       # notwenig, da dauer für den ersten Wert 0 ist und man nicht durch 0 teilen darf
        rpm=int(len(zws1)*30)
    print('Die akutelle Umdrehungszahl pro Minute betärgt:')
    return rpm

def mittelwert2():
    global zws2
    t1=dt.datetime.now()-dt.timedelta(0,aufloesungzm)
    while True:
        if len(zws2)==0:
            break   # Loescht alle Werte die aelter als die dauer der Aufloesung sind
        elif t1>=zws2[0]:
            del zws2[0]
        else:
            break
    n=len(zws1)
    if n>1:     # Berechnet den zeitlichen Abstand zwischen dem ersten und letztem Messwert und berechnet die Umdrehung pro Minute
        dauer=zws2[n-1]-zws2[0]
        rpm=int( (60/dt.timedelta.total_seconds(dauer))*(n/anzahlsensoren))
           # rpm=int(dt.timedelta.total_seconds(dauer)*n)
    elif n==0:
         rpm=0
    else:       # notwenig, da dauer für den ersten Wert 0 ist und man nicht durch 0 teilen darf
        rpm=int(len(zws2)*30)
    print('Die akutelle Umdrehungszahl pro Minute betärgt:')
    return rpm
        
def speichern(turbinerpm, windrpm):
        curs=db.cursor()
        curs.execute("""INSERT INTO Umdrehungen (zeitstempel,rpm , wind) VALUES (NOW(), '%s', '%s')""" %(turbinerpm, windrpm) )
        curs.close()
        db.commit()   


def main():
    #time.sleep(10)
    #db=MySQLdb.connect(host='localhost', user='verlauf', passwd='Turby', db='turbine')
    #print('Datenbank erfolgreich geöffnet')
    #aufloesungzm=int(input('Bitte den gewuenschten Zeitraum zum ermitteln des gleitenden Durchschnitts in Sekunden eingeben: '))
    #aufloesung=int(input('Bitte die gewuenschte Aufloesung in Sekunden eingeben: '))
    t1=timer()
    GPIO.add_event_detect(27, GPIO.BOTH, callback=signalerkennung1, bouncetime=100)
    GPIO.add_event_detect(17, GPIO.BOTH, callback=signalerkennung2, bouncetime=100)
    try:
        # Loop until users quits with CTRL-C
        while True:
           time.sleep(0.01)
        
    except KeyboardInterrupt:
        # Reset GPIO settings
        db.close()
        GPIO.cleanup()
    
        
if __name__ == '__main__':
   global db
   db=MySQLdb.connect(host='localhost', user='verlauf', passwd='Turby', db='turbine')
   #print('Datenbank erfolgreich geöffnet')   
   main()
