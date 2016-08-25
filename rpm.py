#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 21.07.2016

@author: Sander
Listen Durchschnitt bilden und Lise anpassen
'''

# Import required libraries
import datetime as dt
import RPi.GPIO as GPIO
import MySQLdb
import time

#Globale Variablen setzten
global aufloesung 
aufloesung=1 #legt die Messaufloesung in Sekunden fest
global zws  
zws=[]
global abtastrate #legt die Abtastrate in 0,01 sekunden fest
abtastrate=0.01

# Teilt der GPIO Bibliotek mit die GPIO references zu nutzen
GPIO.setmode(GPIO.BCM) 

# Setzt Pin 17 als Inut
GPIO.setup(27 , GPIO.IN)

#erkennt ob an dem GPIO HIGH oder LOW anliegt    
def signalerkennung():
        signal=GPIO.input(27)
        return signal
   
    # Ermittelt aus den Messdaten des Sensors einen 
    # Durchschnittswert für die Dauer der Aufloesung     
def mittelwertmessung():
    i=0
    signal2=3
    while i<aufloesung:
        signal=signalerkennung()
        if signal!=signal2:
            zws.append(1)
        else: 
            zws.append(0)
        i=i+abtastrate
        signal2=signal
        print(str(i)+ '  das aufgenommene Signal ist'+ str(signal) )
        time.sleep(abtastrate)
    
    l=len(zws)
    s=sum(zws)
    rpm=int((60/aufloesung)*(s))
    del zws[:]  
    print('Die akutelle Umdrehungszahl pro Minute betärgt:' + str(rpm) )       
    speichern(rpm)    
    
    '''
    t0=dt.datetime.now()
    t1=t0-dt.timedelta(0,aufloesung)
    zws.append(t0) #fügt den akutellen Timestamp dem Zwischenspeicher für die Timestamps hinzu
    n=len(zws)
    while True:     # Löscht alle Werte die älter als eine Sekunde sind
        if t1>=zws[0]:
            del zws[0]
        else:
            break
    n=len(zws)
    print(n)
    if n>1:     # Berechnet den zeitlichen Abstand zwischen dem ersten und letztem Messwert und berechnet die Umdrehung pro Minute
        dauer=zws[n-1]-zws[0]
        rpm=60/dt.timedelta.total_seconds(dauer)*n      
    else:       # notwenig, da dauer für den ersten Wert 0 ist und man nicht durch 0 teilen darf
        rpm=len(zws)*60  
    return int(rpm)
    '''
def speichern(rpm):
        db=MySQLdb.connect(host='localhost', user='verlauf', passwd='Turby', db='turbine')
        curs=db.cursor()
        curs.execute("""INSERT INTO Umdrehungen (zeitstempel, rpm) VALUES (NOW(), '%s')""" %(rpm) )
        curs.close()
        db.commit()   
   
def main():
    time.sleep(30)
    global rpm
    global aufloesung
    global abtastrate
    print('Datenbank erfolgreich geöffnet')
    #aufloesung=int(input('Bitte die gewuenschte Aufloesung der Daten in Sekunden eingeben: '))
    #abtastrate=0.01*int(input('Bitte die gewuenschte Abtastrate je Sekunden *0,01 eingeben(Bsp: 100=1 s): ')) 
    try:
        # Loop until users quits with CTRL-C    
        while True:
            mittelwertmessung()
    except KeyboardInterrupt:
        # Reset GPIO settings
        db.close()
        GPIO.cleanup()
        
if __name__ == '__main__':   
    main()
            
