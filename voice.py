import speech_recognition as sr
import webbrowser
import os
import subprocess
from googlesearch import search
import spacy
import wikipediaapi
import soundcard as sc
r = sr.Recognizer()
r.energy_threshold=1000
nlp = spacy.load("en_core_web_sm")


def speech_recog():
    
    words = ''
    #TESTING PURPOSES ONLY
    #for index, name in enumerate(sr.Microphone.list_microphone_names()):
        #print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

    #Initialize Microphone
    with sr.Microphone() as source:
        #print("Say anything: ")
        audio = r.listen(source)

    #Attempt a recognition
    try:
        words = r.recognize_google(audio)
    except: 
        print("Recognition failed.")

    words = words.lower()
    print("You said: " + words)
    #sep_words = words.split(' ')
    return words


def define(words):
    doc = nlp(words)
    nouns = [chunk.text for chunk in doc.noun_chunks]
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    nouns = list(set(nouns))
    verbs = list(set(verbs))
    
    for noun in nouns:
        if ' and ' in noun:
            arr = noun.split(' and ')
            for i in arr:
                nouns.append(i)
            continue
        if 'that ' in noun:
            arr = noun.split('that ')
            for i in arr:
                nouns.append(i)
            continue
        if 'the ' in noun:
            arr = noun.split('the ')
            for i in arr:
                nouns.append(i)
            continue
        if 'this ' in noun:
            arr = noun.split('this ')
            for i in arr:
                nouns.append(i)
            continue
        if 'an ' in noun:
            arr = noun.split('an ')
            for i in arr:
                nouns.append(i)
            continue
        if 'a ' in noun:
            arr = noun.split('a ')
            for i in arr:
                nouns.append(i)
            continue
    
    print("Nouns:", nouns)
    print("Verbs:", verbs)

    for noun in nouns:
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(noun)
        if page_py.exists() and noun != '':    
            index = page_py.summary.find('.')
            print(noun.upper() + ': ' + page_py.summary[:index] + '.\n')

    return nouns, verbs


def main():
    file_ = open('test2.txt', 'a')
    while (True):
        words = speech_recog()
        nouns, verbs = define(words)

        file_.writelines([words + '\n', str(nouns) + '\n', str(verbs) + '\n', '\n'])
        #words = 'i am taking classes on cryptography and graph theory on tuesdays.'
        #test()
        print('\n\n\n')
    file_.close()

main()