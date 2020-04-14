#!/usr/bin/python3
# Built using Python 3.7.7
"""
Testing the PicoVoice "porcupine" module for Wake Words.

To end the spate of ALSA warnings/errors that scroll by at startup, you must:
	$ sudo nano /usr/share/alsa/alsa.conf
	- Then edit out  lines that look like "pcm.front cards.pcm.front", or
	  change them to default, for example "pcm.front cards.pcm.default",
	  to match your actual hardware.

The audio reader is low CPU usage, so even though this has a constant primary loop
the CPU use is ~11% according to htop. No need to sleep, in other words.
"""

import sys
import os
import struct
from datetime import datetime
from time import sleep

import pyaudio
from threading import Thread

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../porcupine/binding/python'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../porcupine/resources/util/python'))

from pvporcupine import Porcupine
from util import *

#pvporcupine.create(keywords=pvporcupine.KEYWORDS)

#print(KEYWORDS)
#print(KEYWORD_FILE_PATHS)



class VoiceScanLoop(Thread):
	"""
	Uses PicoVoice's "Porcupine" Wake Word Detection engine to search for wake words and then
	enter an intent scanning loop.
	"""
	def __init__(self,
		library_path,
		model_file_path,
		keyword_file_paths,
		sensitivities,
		input_device_index=None,
		output_path=None):
		"""
		Constructor
		"""
		self.library_path = library_path
		self.model_file_path = model_file_path
		self.keyword_file_paths = keyword_file_paths
		self.sensitivities = sensitivities
		self._output_path = output_path
		self._input_device_index = input_device_index
	
	def run(self):
		"""
		Creates an input audio stream, initializes wake word detection (Porcupine) object, and monitors the audio
		stream for occurrences of the wake word(s). It prints the time of detection for each occurrence and index of
		wake word.
		"""

		keyword_names = list()
		for x in self.keyword_file_paths:
			keyword_names.append(os.path.basename(x).replace('.ppn', '').replace('_compressed', '').split('_')[0])
		num_keywords = len(self.keyword_file_paths)

		audio_stream = None
		pa = None
		porcupine = None
		
		try:
			porcupine = Porcupine(
				library_path=self.library_path,
				model_file_path=self.model_file_path,
				keyword_file_paths=self.keyword_file_paths,
				sensitivities=self.sensitivities)
			
			pa = pyaudio.PyAudio()
			audio_stream = pa.open(
				rate=porcupine.sample_rate,
				channels=1,
				format=pyaudio.paInt16,
				input=True,
				frames_per_buffer=porcupine.frame_length,
				input_device_index=self._input_device_index)

			while True:
				pcm = audio_stream.read(porcupine.frame_length)

				pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

				#if self._output_path is not None:
				#    self._recorded_frames.append(pcm)

				result = porcupine.process(pcm)
				if num_keywords == 1 and result:
					print('[%s] detected keyword' % str(datetime.now()))
					audio_stream.close()
					if self.transcribe():
						audio_stream = pa.open(
							rate=porcupine.sample_rate,
							channels=1,
							format=pyaudio.paInt16,
							input=True,
							frames_per_buffer=porcupine.frame_length,
							input_device_index=self._input_device_index)
				elif num_keywords > 1 and result >= 0:
					print('[%s] detected %s' % (str(datetime.now()), keyword_names[result]))



		except KeyboardInterrupt:
			print('stopping ...')
		finally:
			if porcupine is not None:
				porcupine.delete()

			if audio_stream is not None:
				audio_stream.close()

			if pa is not None:
				pa.terminate()

			if self._output_path is not None and len(self._recorded_frames) > 0:
				recorded_audio = np.concatenate(self._recorded_frames, axis=0).astype(np.int16)
				soundfile.write(self._output_path, recorded_audio, samplerate=porcupine.sample_rate, subtype='PCM_16')
		



def main():
	keyword_file_paths = [KEYWORD_FILE_PATHS[x] for x in ["bumblebee","porcupine"]]
	sensitivities = [0.5] * len(keyword_file_paths)
	VoiceScanLoop(
		LIBRARY_PATH, MODEL_FILE_PATH, keyword_file_paths, sensitivities
	).run()



if __name__ == '__main__':
    main()

