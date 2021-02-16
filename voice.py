import speech_recognition as sr
import webbrowser
import os
import subprocess
from googlesearch import search
import wolframalpha
import spacy
client = wolframalpha.Client('2V87UU-VJHEETLRQE')


def main():
    r = sr.Recognizer()
    r.energy_threshold=1000

    #TESTING PURPOSES ONLY
    #for index, name in enumerate(sr.Microphone.list_microphone_names()):
        #print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

    #Initialize Microphone
    with sr.Microphone() as source:
        print("Say anything: ")
        audio = r.listen(source)



    #Attempt a recognition
    try:
        words = r.recognize_google(audio)
    except: 
        print("Recognition failed.")



    #Activate skill
    words = words.lower()
    print("You said: " + words)
    sep_words = words.split(' ')

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(words)
    print("Nouns:", [chunk.text for chunk in doc.noun_chunks])
    print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
    


main()