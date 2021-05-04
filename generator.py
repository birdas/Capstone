#probabalistic sentence generation
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
    for _ in range(15):
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




string = "In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat; it was a hobbit-hole, and that means comfort. It had a perfectly round door like a porthole, painted green, with a shiny yellow brass knob in the exact middle. The door opened on to a tube-shaped hall like a tunnel: a very comfortable tunnel without smoke, with paneled walls, and floors tiled and carpeted, provided with polished chairs, and lots and lots of pegs for hats and coats – the hobbit was fond of visitors. The tunnel wound on and on, going fairly but not quite straight into the side of the hill – The Hill, as all the people for many miles round called it – and many little round doors opened out of it, first on one side and then on another. No going upstairs for the hobbit: bedrooms, bathrooms, cellars, pantries (lots of these), wardrobes (he had whole rooms devoted to clothes), kitchens, dining-rooms, all were on the same floor, and indeed on the same passage. The best rooms were all on the left-hand side (going in), for these were the only ones to have windows, deep-set round windows looking over his garden, and meadows beyond, sloping down to the river. This hobbit was a very well-to-do hobbit, and his name was Baggins. The Bagginses had lived in the neighbourhood of The Hill for time out of mind, and people considered them very respectable, not only because most of them were rich, but also because they never had any adventures or did anything unexpected: you could tell what a Baggins would say on any question without the bother of asking him. This is a story of how a Baggins had an adventure, and found himself doing and saying things altogether unexpected. He may have lost the neighbours’ respect, but he gained – well, you will see whether he gained anything in the end."
init()
finetune(string)
word_ = input('Input a word to generate a sentence on: ')
while word_ != 'quit':
    markov_chain(word_)
    word_ = input('\n\nInput a word to generate a sentence on: ')
