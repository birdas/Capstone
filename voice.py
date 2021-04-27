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
    init()
    while (True):
        words = speech_recog()
        #words = 'I have classes on graph theory and cryptography on tuesdays and thursdays.'
        print('Sentence: ', words)
        define(words)
        #print(counts)

        finetune(words)
        imp = important(words)
        markov_chain(imp)

        #file_.writelines([words + '\n', str(nouns) + '\n', str(verbs) + '\n', '\n'])
        print('\n\n')
    #file_.close()
    
from tabulate import tabulate
from random import randint, seed
import csv

gamma = {}
bigram_freq = {}
preds = {}
succs = {}

def init():
    global N
    N = 0
    with open('ngrams_words_3.txt', newline='') as lines:
        reader = csv.reader(lines, delimiter = '\t')
        for line in reader:
            line = ' '.join(line)
            line = line.lower().split(' ')
            #print(line[1:4])
            gamma[line[1]] = gamma.get(line[1], 0) + 1
            gamma[line[2]] = gamma.get(line[2], 0) + 1
            gamma[line[3]] = gamma.get(line[3], 0) + 1
            N += 3
            if line[2] not in preds:
                preds[line[2]] = [line[1]]
            else:
                preds[line[2]].append(line[1])

            if line[2] not in succs:
                succs[line[2]] = [line[3]]
            else:
                succs[line[2]].append(line[3])

            bigram_freq[line[1] + ' ' + line[2]] = bigram_freq.get(line[1] + ' ' + line[2], 0) + int(line[0])
            bigram_freq[line[2] + ' ' + line[3]] = bigram_freq.get(line[2] + ' ' + line[3], 0) + int(line[0])


def finetune(words):
    for char in words:
        if char in "?.!,/;:'()":
            words = words.replace(char, '')

    word_list = words.lower().split(' ')
    global N
    N += len(word_list)
    for i in range(len(word_list)):
        gamma[word_list[i]] = gamma.get(word_list[i], 0) + 1
        if i != 0:
            if word_list[i] not in preds:
                preds[word_list[i]] = [word_list[i - 1]]
            else:
                preds[word_list[i]].append(word_list[i - 1])
        if i != len(word_list) - 1:
            bigram_freq[word_list[i] + ' ' + word_list[i + 1]] = bigram_freq.get(word_list[i] + ' ' + word_list[i + 1], 0) + 1
            if word_list[i] not in succs:
                succs[word_list[i]] = [word_list[i + 1]]
            else:
                succs[word_list[i]].append(word_list[i + 1])


def score(w):
    return (pred_score(w) + succ_score(w)) / 2


def pred_score(w): 
    if avg_pred_prob(w) == 0:
        return 0
    gamma_len = len(gamma)
    #Testing
    for y_i in gamma.keys():
        assert prob(y_i, w) >= 0 and prob(y_i, w) <= 1
    #print(avg_pred_prob(w))
    assert avg_pred_prob(w) >= 0 and avg_pred_prob(w) <= 1

    sum_ = sum(((prob(w, y_i) + avg_pred_prob(w)) / avg_pred_prob(w)) ** 2 for y_i in gamma.keys())
    return (sum_ / (gamma_len - 1)) ** .5


def succ_score(w):
    if avg_succ_prob(w) == 0:
        return 0
    gamma_len = len(gamma)
    #Testing
    for y_i in gamma.keys():
        assert prob(y_i, w) >= 0 and prob(y_i, w) <= 1
    #print(avg_pred_prob(w))
    assert avg_pred_prob(w) >= 0 and avg_pred_prob(w) <= 1

    sum_ = sum(((prob(y_i, w) + avg_succ_prob(w)) / avg_succ_prob(w)) ** 2 for y_i in gamma.keys())
    return (sum_ / (gamma_len - 1)) ** .5


def avg_pred_prob(w):
    gamma_len = len(gamma)
    return sum(prob(w, y_i) for y_i in gamma.keys()) / gamma_len


def avg_succ_prob(w):
    gamma_len = len(gamma)
    return sum(prob(y_i, w) for y_i in gamma.keys()) / gamma_len


def prob(w, y_i):
    if w + ' ' + y_i not in bigram_freq:
        return 0
    return bigram_freq[w + ' ' + y_i] / N


def syllable_count(word): #https://stackoverflow.com/questions/46759492/syllable-count-in-python
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count


def important(words):
    best = ''
    best_score = 0.0
    for w in words:
        w_score = score(w)
        if best_score < w_score:
            best = w
            best_score = w_score
        elif best_score == w_score:
            if syllable_count(best) < syllable_count(w):
                best = w
                best_score = w_score
            elif syllable_count(best) == syllable_count(w):
                if len(best) < len(w):
                    best = w
                    best_score = w_score
    return best


def display():
    data = [[w, gamma[w], score(w), syllable_count(w), len(w)] for w in gamma.keys()]
    print(tabulate(data, headers = ['Word', 'Freq', 'Score', 'Syllables', 'Length']))
    print('\nMost important word is:', important(list(gamma.keys())))


def markov_chain(word_):
    sen = ''

    if word_ not in gamma.keys():
        return

    word = word_
    #seed(27) #Only for testing
    for _ in range(20):
        if word == "n't":
            sen += word
        else:
            sen += ' ' + word
        
        markov = {}
        sum_ = 0
        for s in gamma.keys():
            val = prob(word, s)
            if val != 0:
                markov[s] = val
                sum_ += markov[s]
        #print('Markov:', markov)
        #print('Sum:', sum_)
        prev = 0
        chain = {}
        for s in markov.keys():
            chain[s] = (markov[s] / sum_) + prev
            prev = chain[s]
        pick = randint(0, 10000000000000) / 10000000000000
        #print('Chain:', chain)
        for s in chain.keys():
            if pick <= chain[s]:
                word = s
                break
        #print('Next word:', word)
        #print('\n')
    sen = sen[1:]
    print('Generated sentence of of "' + word_ + '" is:', sen)

    
main()