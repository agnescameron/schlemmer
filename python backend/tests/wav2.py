from playsound import playsound
from threading import Thread
import time

def play(sound):
    playsound(sound)
    # time.sleep(0.2)
    

for i in range(0, 5):
	play('../../sounds/kung-fu/punch1.wav')
