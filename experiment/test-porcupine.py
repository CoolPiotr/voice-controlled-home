#!/usr/bin/python3
# Built using Python 3.7.7
"""

"""

import porcupine
import pyaudio

pvporcupine.create(keywords=pvporcupine.KEYWORDS)



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
	
	def run(self):
		"""
		Creates an input audio stream, initializes wake word detection (Porcupine) object, and monitors the audio
		stream for occurrences of the wake word(s). It prints the time of detection for each occurrence and index of
		wake word.
		"""
		'''
        num_keywords = len(self._keyword_file_paths)

        keyword_names = list()
        for x in self._keyword_file_paths:
            keyword_names.append(os.path.basename(x).replace('.ppn', '').replace('_compressed', '').split('_')[0])
		'''
		porcupine = None
		
		try:
			porcupine = Porcupine(
				library_path=self._library_path,
				model_file_path=self._model_file_path,
				keyword_file_paths=self._keyword_file_paths,
				sensitivities=self._sensitivities)
			
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
	VoiceScanLoop(
	).run()



if __name__ == '__main__':
    main()

