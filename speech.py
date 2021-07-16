import time
from azure.cognitiveservices.speech import SpeechConfig
import azure.cognitiveservices.speech as speechsdk

key1 = "my-super-secret-key"
region = "eastus"
wav_file = "filename.wav"
len_of_file = 4140
mapping = {} 

def record():
    # Overwrite raw JSON file with all word count results
    with open("raw.json", "w") as outfile:
        outfile.write(str(mapping))

    # Sort and write sorted list to JSON file
    s = sorted(mapping.items(), key=lambda i:i[1], reverse=True)
    with open("res.json", "w") as outfile:
        outfile.write(str(s))

def parse_result(res, m):
    # Take a single-line result, parses and includes result in result map m
    # First write the raw text result to text.txt
    with open("text.txt", "a") as outfile:
        outfile.write(res + "\n")
    sp = res.split(" ")
    for i in sp:
        word = "" # We re-build each word from a blank string
        for j in i: # Loop through each character
            if j.isalpha(): # Avoid non-letters
                word += j.lower() # Convert result to lowercase
        m[word] = m.get(word, 0)+1 # Increase value in dict by one, or initialize to one
    record()

speech_config = SpeechConfig(subscription=key1, region=region)
audio_input = speechsdk.AudioConfig(filename=wav_file)  
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
speech_recognizer.session_stopped.connect(lambda evt: print('\nSESSION STOPPED {}'.format(evt)))
speech_recognizer.recognized.connect(lambda evt: parse_result(evt.result.text, mapping))

try:
    while True:
        speech_recognizer.start_continuous_recognition()
        time.sleep(len_of_file)
        speech_recognizer.stop_continuous_recognition()

except KeyboardInterrupt:
        speech_recognizer.session_started.disconnect_all()
        speech_recognizer.recognized.disconnect_all()
        speech_recognizer.session_stopped.disconnect_all()
