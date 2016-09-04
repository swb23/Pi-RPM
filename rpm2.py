#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 21.07.2016

@author: Sander
Listen Durchschnitt bilden und Lise anpassen
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
aufloesungzm=5
global anzahlsensoren
anzahlsensoren=1
global zws  
zws=[]
global db


# Teilt der GPIO Bibliotek mit die GPIO references zu nutzen
GPIO.setmode(GPIO.BCM)

# Setzt Pin 17 als Inut
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
            rpm=mittelwert()
            
            print(rpm)
            speichern(rpm)
            
       
    # Ermittelt aus den Messdaten des Sensors einen Durchschnittswert für die Dauer der Aufloesung     
def mittelwert():
    global zws
    t1=dt.datetime.now()-dt.timedelta(0,aufloesungzm)
    while True:
        if len(zws)==0:
            break   # Loescht alle Werte die aelter als die dauer der Aufloesung sind
        elif t1>=zws[0]:
            del zws[0]
        else:
            break
    n=len(zws)
    if n>1:     # Berechnet den zeitlichen Abstand zwischen dem ersten und letztem Messwert und berechnet die Umdrehung pro Minute
	dauer=zws[n-1]-zws[0]
	rpm=int( (60/dt.timedelta.total_seconds(dauer))*(n/anzahlsensoren))
	       # rpm=int(dt.timedelta.total_seconds(dauer)*n)
    elif n==0:
         rpm=0
    else:       # notwenig, da dauer für den ersten Wert 0 ist und man nicht durch 0 teilen darf
	 rpm=int(len(zws)*30)
   # print('Die akutelle Umdrehungszahl pro Minute betärgt:')
    return rpm
    
   

def signalerkennung(channel):
    global zws
    t0=dt.datetime.now()
    zws.append(t0) #fuegt den akutellen Timestamp dem Zwischenspeicher für die Timestamps hinzu
        
def speichern(rpm):
        curs=db.cursor()
        curs.execute("""INSERT INTO Umdrehungen (zeitstempel, rpm) VALUES (NOW(), '%s')""" %(rpm) )
        curs.close()
        db.commit()   


def main():
    time.sleep(10)
    global rpm
    global aufloesungzm
    global aufloesung
    global db
    db=MySQLdb.connect(host='localhost', user='verlauf', passwd='Turby', db='turbine')
    #print('Datenbank erfolgreich geöffnet')
    #aufloesungzm=int(input('Bitte den gewuenschten Zeitraum zum ermitteln des gleitenden Durchschnitts in Sekunden eingeben: '))
    #aufloesung=int(input('Bitte die gewuenschte Aufloesung in Sekunden eingeben: '))
    t1=timer()
    GPIO.add_event_detect(17, GPIO.FALLING, callback=signalerkennung)   
    try:
        # Loop until users quits with CTRL-C
        while True:
           time.sleep(0.01)
        
    except KeyboardInterrupt:
        # Reset GPIO settings
        db.close()
        GPIO.cleanup()
    
        
if __name__ == '__main__':   
    main()
            
