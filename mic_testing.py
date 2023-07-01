

# pour regler le pb volume 0 micro:

#     - check pyaudio et portaudio => X
#     - conda install nwani::portaudio nwani::pyaudio (commande révolutionnaire d'un sympatique petit indien) => XX
#     - pip install Pyaudio => XX
#     - conda install portaudio => X



# procédure solution : 

# reboot sans micro
# brancher micro 
# SET AS FALLBACK !!
#config => digital stereo (hdmi) output 
# analog stereo duplex


# lspci -v | grep -A1 -i audio => liste les périphériques audio détectés par le système en utilisant la commande lspci, qui affiche les informations sur les périphériques PCI, et en filtrant les lignes contenant le mot "audio". L'option -A1 affiche également la ligne suivante après chaque correspondance.
# aplay -l  =>  liste les périphériques audio disponibles sur le système. Elle utilise la commande aplay pour afficher les informations sur les périphériques de lecture audio, tels que les cartes son et les périphériques de sortie.
# pacmd list-sources   => liste des sources audio disponibles pour le serveur de son PulseAudio. Elle donne des informations détaillées sur les sources audio, y compris les périphériques d'entrée tels que les microphones

# pour gerer pulsaudio => pacmd et pactl

# Sur linux, le son est géré par PulseAudio
# PulseAudio Server : Le serveur PulseAudio s'exécute en arrière-plan et gère toutes les opérations liées au son.




# wav encodage de qualité, élevé



# If ``device_index`` is unspecified or ``None``, the default microphone is used as the audio source. Otherwise, ``device_index`` should be the index of the device to use for audio input.

# A device index is an integer between 0 and ``pyaudio.get_device_count() - 1`` (assume we have used ``import pyaudio`` beforehand) inclusive. It represents an audio device such as a microphone or speaker. See the `PyAudio documentation <http://people.csail.mit.edu/hubert/pyaudio/docs/>`__ for more details.

# The microphone audio is recorded in chunks of ``chunk_size`` samples, at a rate of ``sample_rate`` samples per second (Hertz). If not specified, the value of ``sample_rate`` is determined automatically from the system's microphone settings.

# Higher ``sample_rate`` values result in better audio quality, but also more bandwidth (and therefore, slower recognition). Additionally, some CPUs, such as those in older Raspberry Pi models, can't keep up if this value is too high.

# Higher ``chunk_size`` values help avoid triggering on rapidly changing ambient noise, but also makes detection less sensitive. This value, generally, should be left at its default.




# pavucontrol => configuration ??
# ~/.config/pulse ??
# cat /etc/pulse defaut.pa 
# cat /etc/pulse daemon.conf




#================== 


# # =====example 1=============

# import pyaudio
# pa = pyaudio.PyAudio()
# print(pa.get_default_input_device_info())
# print('\n\n')
# print(pa.get_device_count())
# print('\n\n')



# # =====example 2=============


import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print((i,dev['name'],dev['maxInputChannels']))



# output >

# (0, 'HDA Intel HDMI: 1 (hw:0,7)', 0)
# (1, 'HDA Intel HDMI: 2 (hw:0,8)', 0)
# (2, 'HDA Intel HDMI: 3 (hw:0,9)', 0)
# (3, 'HDA Intel HDMI: 4 (hw:0,10)', 0)
# (4, 'HDA Intel PCH: ALC3235 Analog (hw:1,0)', 0)
# (5, 'pulse', 32)
# (6, 'default', 32)

# output après reboot (sans micro branché)>
# (0, 'HDA Intel HDMI: 0 (hw:0,3)', 0)
# (1, 'HDA Intel HDMI: 1 (hw:0,7)', 0)
# (2, 'HDA Intel HDMI: 2 (hw:0,8)', 0)
# (3, 'HDA Intel HDMI: 3 (hw:0,9)', 0)
# (4, 'HDA Intel HDMI: 4 (hw:0,10)', 0)
# (5, 'HDA Intel PCH: ALC3235 Analog (hw:1,0)', 2)
# (6, 'hdmi', 0)
# (7, 'pulse', 32)
# (8, 'default', 32)

#avec micro 
# (0, 'HDA Intel HDMI: 1 (hw:0,7)', 0)
# (1, 'HDA Intel HDMI: 2 (hw:0,8)', 0)
# (2, 'HDA Intel HDMI: 3 (hw:0,9)', 0)
# (3, 'HDA Intel HDMI: 4 (hw:0,10)', 0)
# (4, 'pulse', 32)
# (5, 'default', 32)





# =====example 3=============

import pyaudio
import wave 


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

audio = pyaudio.PyAudio()

# Ouverture du flux audio en entrée
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=7)

frames = []

print("Enregistrement en cours. Appuyez sur Ctrl+C pour arrêter.")

try:
    # Lecture du flux audio et ajout des données dans la liste des frames
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
except KeyboardInterrupt:
    pass

print("Enregistrement terminé.")

# Arrêt et fermeture du flux audio
stream.stop_stream()
stream.close()
audio.terminate()

# Sauvegarde des frames dans un fichier WAV
wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b"".join(frames))
wf.close()

print("Audio enregistré dans", WAVE_OUTPUT_FILENAME)


# =====example 4=============


# import custom_speech_recognition as sr

# # obtain audio from the microphone
# r = sr.Recognizer()

# r.dynamic_energy_threshold = False
# r.energy_threshold = 15000

# with sr.Microphone(device_index=5) as source:
#     print("Say something!")
#     audio = r.listen(source)



# # write audio to a WAV file
# with open("microphone-results.wav", "wb") as f:
#     f.write(audio.get_wav_data())

