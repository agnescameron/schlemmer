import pygame as pg
import time

# pg.mixer.pre_init(44100, 16, 2, 4096) 
pg.mixer.init()
pg.init()

drum0 = pg.mixer.Sound("../../sounds/japanese-percussion/tsuzumi.wav")
drum1 = pg.mixer.Sound("../../sounds/japanese-percussion/biz.wav")
drum2 = pg.mixer.Sound("../../sounds/japanese-percussion/taiko.wav")
drum3 = pg.mixer.Sound("../../sounds/japanese-percussion/hyoshigi.wav")
drum4 = pg.mixer.Sound("../../sounds/japanese-percussion/kagura.wav")

a = 1

drums = [drum0, drum1, drum2, drum3, drum4]

pg.mixer.set_num_channels(50)
channel0 = pg.mixer.Channel(0) # argument must be int
channel1 = pg.mixer.Channel(1)
channel2 = pg.mixer.Channel(2)
channel3 = pg.mixer.Channel(3)
channel4 = pg.mixer.Channel(4)


while True:
	channel0.play(drums[0])
	channel1.play(drums[1])
	channel2.play(drums[2])
	channel3.play(drums[3])
	channel4.play(drums[4])