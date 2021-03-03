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
    
    bad_words = [' and ', 'that ', 'the ', 'this ', 'an ', 'a ']
    clean_nouns = []
    for noun in nouns:
        for bad_word in bad_words:
            split = False
            if bad_word in noun and not split:
                arr = noun.split(bad_word)
                split = True
                for i in arr:
                    if i != '':
                        clean_nouns.append(i)
                continue
        if not split:
            clean_nouns.append(noun)

    print("Nouns:", nouns)
    print("Verbs:", verbs)


    for noun in clean_nouns:
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(noun)
        if page_py.exists() and noun != '':    
            index = page_py.summary.find('.')
            print('\033[1m' + noun.upper() + ':\033[0m ' + page_py.summary[:index] + '.\n')

    return nouns, verbs


def main():
    file_ = open('test2.txt', 'a')
    while (True):
        words = speech_recog()
        nouns, verbs = define(words)

        file_.writelines([words + '\n', str(nouns) + '\n', str(verbs) + '\n', '\n'])
        #words = 'i am taking classes on cryptography and graph theory on tuesdays.'
        #test()
        print('\n\n')
    file_.close()

main()