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

counts = {}
calibrated = False

def speech_recog():
    
    global calibrated
    words = ''
    #TESTING PURPOSES ONLY
    #for index, name in enumerate(sr.Microphone.list_microphone_names()):
        #print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

    #Initialize Microphone
    with sr.Microphone() as source:
        #print("Say anything: ")
        if not calibrated:
            calibrated = True
            print('Calibrating...')
            r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    #Attempt a recognition
    try:
        words = r.recognize_google(audio)
    except: 
        print("Recognition failed.")

    #print("You said: " + words)
    #sep_words = words.split(' ')
    return words


def define(words):
    words = words.lower()
    doc = nlp(words)

    noun_chunks = [chunk.text for chunk in doc.noun_chunks]
    nouns = [token.lemma_ for token in doc if token.pos_ == 'NOUN']
    verbs = [token.lemma_ for token in doc if token.pos_ == 'VERB']
    adverbs = [token.lemma_ for token in doc if token.pos_ == 'ADV']
    adjectives = [token.lemma_ for token in doc if token.pos_ == 'ADJ']

    noun_chunks = list(set(noun_chunks))
    nouns = list(set(nouns))
    verbs = list(set(verbs))
    adverbs = list(set(adverbs))
    adjectives = list(set(adjectives))
    
    bad_words = [' and ', 'that ', 'the ', 'this ', 'an ', 'a ', 'my ']
    clean_nouns = []
    for noun in noun_chunks: #loop through chunks
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
    for noun in nouns: #loop through nouns
        if noun + 's' not in noun_chunks and noun + 'es' not in noun_chunks and noun not in noun_chunks:
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

    print('Nouns and Noun Chunks:', clean_nouns)
    print('Verbs:', verbs)
    print('Adverbs:', adverbs)
    print('Adjectives:', adjectives)
    
    #define
    for noun in clean_nouns:
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(noun)
        if page_py.exists() and noun != '':    
            index = page_py.summary.find('.')
            if 'may refer to' not in page_py.summary[:index].lower():
                print('\033[1m' + noun.upper() + ':\033[0m ' + page_py.summary[:index] + '.\n')
            else: 
                print('\033[1m' + noun.upper() + ':\033[0m Too ambiguous for definition.\n')

    incrementCounts(clean_nouns)
    incrementCounts(verbs)
    incrementCounts(adverbs)
    incrementCounts(adjectives)
    
    return nouns, verbs


def incrementCounts(nouns):
    for key in nouns:
        counts[key] = counts.get(key, 0) + 1


def main():
    
    #file_ = open('test4.txt', 'a')
    while (True):
        words = speech_recog()
        #words = 'I have classes on graph theory and cryptography on tuesdays and thursdays.'
        print('Sentence: ', words)
        nouns, verbs = define(words)
        print(counts)

        #file_.writelines([words + '\n', str(nouns) + '\n', str(verbs) + '\n', '\n'])
        print('\n\n')
    #file_.close()
    
    
main()