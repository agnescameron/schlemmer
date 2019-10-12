import logging
import threading
import pygame as pg
import time

pg.mixer.init()
pg.init()
pg.mixer.set_num_channels(50)



drum1 = pg.mixer.Sound("../../sounds/japanese-percussion/biz.wav")
drum4 = pg.mixer.Sound("../../sounds/japanese-percussion/taiko.wav")
drum2 = pg.mixer.Sound("../../sounds/japanese-percussion/hyoshigi.wav")
drum3 = pg.mixer.Sound("../../sounds/japanese-percussion/kagura.wav")
drum0 = pg.mixer.Sound("../../sounds/japanese-percussion/tsuzumi.wav")
drums = [drum0, drum1, drum2, drum3, drum4]


def channel(num, pause):
	while True:
		drums[num].play()
		time.sleep(num+0.2)

if __name__ == "__main__":
	thread = threading.Thread(target=printFile, args=(0, ))
	thread.start()

	for i in range (0, len(drums)):
		thread = threading.Thread(target=channel, args=(i, i))
		thread.start()
