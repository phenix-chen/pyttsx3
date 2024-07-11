"""PyAudio Example: Play a wave file."""
import os
import wave
import pyaudio

# CHUNK = 1024

# if len(sys.argv) < 2:
#     print(f"Plays a wave file. Usage: {sys.argv[0]} filename.wav")
#     sys.exit(-1)

# with wave.open(sys.argv[1], "rb") as wf:
#     # Instantiate PyAudio and initialize PortAudio system resources (1)
#     p = pyaudio.PyAudio()

#     # Open stream (2)
#     stream = p.open(
#         format=p.get_format_from_width(wf.getsampwidth()),
#         channels=wf.getnchannels(),
#         rate=wf.getframerate(),
#         output=True,
#     )

#     # Play samples from the wave file (3)
#     # while len(data := wf.readframes(-1)):  # Requires Python 3.8+ for :=
#     #     stream.write(data)
#     data = wf.readframes(-1)
#     t1 = time.time()
#     stream.write(data)
#     t2 = time.time()
#     stream.write(data)
#     t3 = time.time()
#     stream.write(data)
#     t4 = time.time()
#     print(t4 - t3, t3 - t2, t2 - t1)

#     # Close stream (4)
#     stream.close()

#     # Release PortAudio system resources (5)
#     p.terminate()




class Audio:
    def __init__(self) -> None:
        p = pyaudio.PyAudio()
        # self.audios = {"1": self.preload_audio("1.wav")}
        # self.audios["2"] = self.preload_audio("2.wav")
        # self.audios = self._preload_number_audios()
        self.audios = self._preload_audios()

        with wave.open("number_audios/1.wav", "rb") as wf:
            # Instantiate PyAudio and initialize PortAudio system resources (1)
            p = pyaudio.PyAudio()

            print(wf.getframerate())
            # Open stream (2)
            self.stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
            )

    def _preload_number_audios(self):
        audios = {}
        for i in range(0, 13):
            filename = f"number_audios/{i}.wav"
            audios[str(i)] = self._preload_audio(filename)
        return audios

    def _preload_audios(self):
        audios = {}
        directory = "number_audios"
        for filename in os.listdir(directory):
            if filename.endswith(".wav"):
                key = ".".join(filename.split(".")[:-1])
                audios[key] = self._preload_audio(f"{directory}/{filename}")
        return audios

    def _preload_audio(self, audio_file):
        print(audio_file)
        with wave.open(audio_file, "rb") as wf:
            data = wf.readframes(-1)
        return data

    def play_audio(self, number):
        audio = self.audios.get(number, None)
        if audio:
            self.stream.write(audio)

    def play_audio_numbers(self, numerals):
        for numeral in numerals:
            self.play_audio(str(numeral))


if __name__ == "__main__":
    voice = Audio()
    voice.play_audio("0")
    voice.play_audio("1")
    voice.play_audio("2")
    voice.play_audio("3")
    voice.play_audio("4")
    voice.play_audio("5")
    voice.play_audio("6")
    voice.play_audio("7")
    voice.play_audio("8")
    voice.play_audio("9")
    voice.play_audio("10")
    voice.play_audio("11")
    voice.play_audio("12")
