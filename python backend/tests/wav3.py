# from PyObjCTools import NSSound
import pydub
from pydub.playback import play
import time

# "../../sounds/kung-fu/punch1.wav"

sound0 = pydub.AudioSegment.from_wav("../../sounds/japanese-percussion/biz.wav")
sound1 = pydub.AudioSegment.from_wav("../../sounds/japanese-percussion/hyoshigi.wav")
sound2 = pydub.AudioSegment.from_wav("../../sounds/japanese-percussion/kagura.wav")
sound3 = pydub.AudioSegment.from_wav("../../sounds/japanese-percussion/taiko.wav")
sound4 = pydub.AudioSegment.from_wav("../../sounds/japanese-percussion/tsuzumi.wav")

sounds = [sound0, sound1, sound2, sound3, sound4]

for i in range (0, 5):
	play(sounds[i])
	# time.sleep(0.1*i)