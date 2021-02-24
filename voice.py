import speech_recognition as sr
import webbrowser
import os
import subprocess
from googlesearch import search
import wolframalpha
import spacy
import wikipediaapi
client = wolframalpha.Client('2V87UU-VJHEETLRQE')


def speech_recog():
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

    words = words.lower()
    #print("You said: " + words)
    #sep_words = words.split(' ')
    return words


def define(words):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(words)
    nouns = [chunk.text for chunk in doc.noun_chunks]
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    #print("Nouns:", nouns)
    #print("Verbs:", verbs)


    for noun in nouns:
        if ' and ' in noun:
            arr = noun.split(' and ')
            for i in arr:
                nouns.append(i)
            continue
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(noun)
        index = page_py.summary.find('.')
        print(noun.upper() + ': ' + page_py.summary[:index] + '.\n')


def main():
    #words = speech_recog()
    words = 'i am taking classes on cryptography and graph theory on tuesdays.'
    define(words)
    

main()