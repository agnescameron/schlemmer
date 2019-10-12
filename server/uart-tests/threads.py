import logging
import threading
import pygame as pg
import time

pg.mixer.init()
pg.init()
pg.mixer.set_num_channels(50)


drum0 = pg.mixer.Sound("../../sounds/japanese-percussion/biz.wav")
drum1 = pg.mixer.Sound("../../sounds/japanese-percussion/taiko.wav")
drum2 = pg.mixer.Sound("../../sounds/japanese-percussion/hyoshigi.wav")
drum3 = pg.mixer.Sound("../../sounds/japanese-percussion/kagura.wav")
drums = [drum0, drum1, drum2, drum3]
 
def thread_function(num):
	logging.info("Thread %s: starting", num)
	while True:
		drums[num].play()
		time.sleep(num)
	logging.info("Thread %s: finishing", num)

if __name__ == "__main__":
	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO,
	                 datefmt="%H:%M:%S")

	logging.info("Main    : before creating thread")
	for i in range (0, len(drums)):
		thread = threading.Thread(target=thread_function, args=(i,))
		thread.start()		
	logging.info("Main    : wait for the thread to finish")
	# x.join()
	logging.info("Main    : all done")