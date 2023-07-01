
from io import BytesIO
import openai as openai

from elevenlabs import generate, play, Voices, stream
from elevenlabs import set_api_key
import custom_speech_recognition as sr
import time

from playsound import playsound

from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")


class VoiceAssistant:

    def __init__(self):
        # Set your OpenAI API key
        openai.api_key = OPENAI_API_KEY

        # elevenlabs api key
        set_api_key(ELEVEN_API_KEY)

        self.total_token = 0





        # Initialize the assistant's history
        self.history = [
            {"role": "system", "content": """- Act as a French human named Valentin and embody the role of the owner of Les Trois Cafés, a renowned gourmet restaurant. You are responsible for managing phone conversations with potential customers.
 Les Trois Cafés is a restaurant located in the center of Montpellier, specializing in meats and offering a vegetarian menu. There is an option to dine outside on the terrace.
Tomorrow evening: five seats available.
The day after tomorrow: ten seats available.
Every evening next week.
Write the number in words. Maintain a professional and courteous demeanor during the call. Provide concise and clear responses. You speak French. Do not respond if you don't know the answer. You only need a name to validate a reservation, and a confirmation SMS will be sent. Remember that you are talking to a human, so if their response is incomplete, ask them to provide more details or clarify their request. Here is the first sentence of the discussion from the restaurateur Valentin : "Bonjour ici le restaurant des trois cafés, comment je peux vous aider ?"
"""}
        ]

        self.start_time_total = 0.0
        

    def listen(self, r, m):
        """
        Records audio from the user and transcribes it.
        """

        print("Listening...")

        
    
        with m as source:
            audio = r.listen(source)

        start_time = time.time()
        self.start_time_total = time.time()

        wav_data = BytesIO(audio.get_wav_data())
        wav_data.name = "SpeechRecognition_audio.wav"

        transcript = openai.Audio.transcribe("whisper-1", wav_data)
        transcript = transcript["text"]

        end_time = time.time()
        execution_time = end_time - start_time
        print('Temps pour de la fonction listen (detection + whisper): ', execution_time)

        print("Whisper API thinks you said: ", transcript)

    
        return transcript

    def think(self, text):
        start_time = time.time()

        """
        Generates a response to the user's input.
        """
        # Add the user's input to the assistant's history
        self.history.append({"role": "user", "content": text})

        # print(self.history)
        # Send the conversation to the GPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=self.history,
            temperature=0.5
        )

        rappel = "Act like a human named Valentin. You are the owner of the restaurant 'les trois cafés' in Montpellier. You are in conversation with a customer who wants to book. Make short answers. You speak French. Don't say 'Hello' everytimes"

        # Extract the assistant's response from the API response
        message = dict(response.choices[0])['message']['content']
        self.total_token += dict(response.usage)['total_tokens']
        end_time = time.time()
        execution_time = end_time - start_time
        print('Temps pour de la fonction think (gpt3.5-turbo): ', execution_time)
        self.history.append({"role": "assistant", "content": message})
        self.history.append({"role": "system", "content": rappel})
        print('Assistant: ', message)
        return message
    




    def speak(self, text):
        start_time = time.time()

        # """"
        # Converts text to speech and plays it.
        # """

        audio_stream = generate(
            text=text,
            stream=True,
            voice="Antoni",
            model='eleven_multilingual_v1',
        )

        end_time = time.time()
        execution_time = end_time - start_time
        print('Temps pour de la fonction speak (elevenLabs): ', execution_time)

        end_time_total = time.time()
        execution_time_total = end_time_total - self.start_time_total
        print('Temps Total pour la réponse: ', execution_time_total)


        stream(audio_stream)


assistant = VoiceAssistant()






# obtain audio from the microphone
r = sr.Recognizer()
m = sr.Microphone()#device_index=8)

  
# r.energy_threshold = 300  # minimum audio energy to consider for recording
r.dynamic_energy_threshold = True
r.dynamic_energy_adjustment_damping =0.15
r.dynamic_energy_ratio = 2
r.pause_threshold = 0.8  # seconds of non-speaking audio before a phrase is considered complete
r.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout
r.phrase_threshold = 0.1  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
r.non_speaking_duration = 0.1  # seconds of non-speaking audio to keep on both sides of the recording


            
playsound('pre_records/bonjour.mp3')
audio_attente = ['pre_records/euh.mp3', 'pre_records/hmm.mp3', 'pre_records/hum.mp3']

def main():
    while True:
        r.energy_threshold = 5000
        r.dynamic_energy_threshold = True


        
        text = assistant.listen(r, m)


        response = assistant.think(text)
        assistant.speak(response)
        
        print(assistant.history)
        print ("nombre total de token= ", assistant.total_token)

if __name__ == "__main__":
    main()









# ==================== NOTES =================


#================ Prompt V1 =====================
        #  {"role": "system", "content": """
        #     Agis comme un humains Français du nom de Ben, et incarne le rôle du propriétaire du restaurant des trois mousquetaires, un restaurant gastronomique réputé. Tu dois gérer une conversation téléphonique avec des clients potentiels.
        #     Dans ton restaurant, les trois mousquetaires, voici les disponibilités:
        #     - demain vingt heures dix places disponibles
        #     - demain vingt et une heure cinq places disponibles
        #     - semaine prochaine pas possible
        #     Tu dois être professionel et courtois pendant l'appel.
        #     Fais des réponse courte et clair.
        #     Tu parle à un être humain, donc si sa réponse n'est pas complète, demande lui de la compléter, ou demandez plus de détails au besoin.
        #     """}

#================ Prompt V2 =====================

        # La conversation suivante est une discussion entre un humains Français du nom de Ben, propriétaire du restaurant des trois mousquetaires, un restaurant gastronomique réputé. Il gère une conversation téléphonique avec des clients potentiels.
        # Les Trois cafés est un restaurant en plein centre de Montpellier, avec une spécialité pour les viandes, il a un menu végétarien.
        # Il y a une possibilité de manger dehors sur la terrasse. 
        # Dans son restaurant, les trois mousquetaires, voici les disponibilités:
        # - demain soir:places
        # - après demain: dix places
        # - tous les soirs de la semaines prochaine.
        # Il demande qu'une seul chose à la fois à son client
        # Il est professionel et courtois pendant l'appel.
        # Il fais des réponses courtes.
        # Il parle en Français.
        # il ne répond pas si il ne connait pas la réponse
        # Il a seulement besoin d'un nom pour valider une réservation et un sms de confirmation sera envoyé.
        # Le restaurateur peut demander au client de compléter des demandes ou avoir plus de détail au besoin.

#================ Prompt V3 =====================

#  {"role": "system", "content": """
#     Agis comme un humains Français du nom de Valentin, et incarne le rôle du propriétaire du restaurant des trois mousquetaires, un restaurant gastronomique réputé. Tu dois gérer une conversation téléphonique avec des clients potentiels.
#     Les Trois cafés est un restaurant en plein centre de Montpellier, avec une spécialité pour les viandes, il a un menu végétarien.  Il y a une possibilité de manger dehors sur la terrasse. 
#    - demain soir: 5 places
#    - après demain: dix places
#    - tous les soirs de la semaines prochaine.
#     Tu dois être professionel et courtois pendant l'appel.
#     Fais des réponse courte et clair.
#     Tu parles Français. 
#     Tu  ne réponds pas si tu ne connais pas la réponse
#     Tu as seulement besoin d'un nom pour valider une réservation et un sms de confirmation sera envoyé.
#     Tu parle à un être humain, donc si sa réponse n'est pas complète, demande lui de la compléter, ou demandez plus de détails au besoin.
#     """}


# Agis comme un humain du nom de Valentin.Tu es propriétaire du restaurant des trois mousquetaires. Tu es en conversation avec un client qui veux réserver. Fais des réponses courtes. Tu parles Français.
