#probabalistic sentence generation
from tabulate import tabulate
from random import randint, seed
import csv

def __init__(self):
    self.gamma = {}
    self.bigram_freq = {}
    self.preds = {}
    self.succs = {}
    init(self)

def init(self):
    global N
    N = 0
    with open('ngrams_words_3.txt', newline='') as lines:
        reader = csv.reader(lines, delimiter = '\t')
        for line in reader:
            line = ' '.join(line)
            line = line.lower().split(' ')
            #print(line[1:4])
            self.gamma[line[1]] = self.gamma.get(line[1], 0) + 1
            self.gamma[line[2]] = self.gamma.get(line[2], 0) + 1
            self.gamma[line[3]] = self.gamma.get(line[3], 0) + 1
            N += 3
            if line[2] not in self.preds:
                self.preds[line[2]] = [line[1]]
            else:
                self.preds[line[2]].append(line[1])

            if line[2] not in self.succs:
                self.succs[line[2]] = [line[3]]
            else:
                self.succs[line[2]].append(line[3])

            self.bigram_freq[line[1] + ' ' + line[2]] = self.bigram_freq.get(line[1] + ' ' + line[2], 0) + int(line[0])
            self.bigram_freq[line[2] + ' ' + line[3]] = self.bigram_freq.get(line[2] + ' ' + line[3], 0) + int(line[0])


def finetune(self, words):
    for char in words:
        if char in "?.!,/;:'()":
            words = words.replace(char, '')

    word_list = words.lower().split(' ')
    global N
    N += len(word_list)
    for i in range(len(word_list)):
        self.gamma[word_list[i]] = self.gamma.get(word_list[i], 0) + 1
        if i != 0:
            if word_list[i] not in self.preds:
                self.preds[word_list[i]] = [word_list[i - 1]]
            else:
                self.preds[word_list[i]].append(word_list[i - 1])
        if i != len(word_list) - 1:
            self.bigram_freq[word_list[i] + ' ' + word_list[i + 1]] = self.bigram_freq.get(word_list[i] + ' ' + word_list[i + 1], 0) + 1
            if word_list[i] not in self.succs:
                self.succs[word_list[i]] = [word_list[i + 1]]
            else:
                self.succs[word_list[i]].append(word_list[i + 1])


def score(self, w):
    return (pred_score(self, w) + succ_score(self, w)) / 2


def pred_score(self, w): 
    if avg_pred_prob(self, w) == 0:
        return 0
    gamma_len = len(self.gamma)
    #Testing
    for y_i in self.gamma.keys():
        assert prob(self, y_i, w) >= 0 and prob(self, y_i, w) <= 1
    #print(avg_pred_prob(w))
    assert avg_pred_prob(self, w) >= 0 and avg_pred_prob(self, w) <= 1

    sum_ = sum(((prob(self, w, y_i) + avg_pred_prob(self, w)) / avg_pred_prob(self, w)) ** 2 for y_i in self.gamma.keys())
    return (sum_ / (gamma_len - 1)) ** .5


def succ_score(self, w):
    if avg_succ_prob(self, w) == 0:
        return 0
    gamma_len = len(self.gamma)
    #Testing
    for y_i in self.gamma.keys():
        assert prob(self, y_i, w) >= 0 and prob(self, y_i, w) <= 1
    #print(avg_pred_prob(w))
    assert avg_pred_prob(self, w) >= 0 and avg_pred_prob(self, w) <= 1

    sum_ = sum(((prob(self, y_i, w) + avg_succ_prob(self, w)) / avg_succ_prob(self, w)) ** 2 for y_i in self.gamma.keys())
    return (sum_ / (gamma_len - 1)) ** .5


def avg_pred_prob(self, w):
    gamma_len = len(self.gamma)
    return sum(prob(self, w, y_i) for y_i in self.gamma.keys()) / gamma_len


def avg_succ_prob(self, w):
    gamma_len = len(self.gamma)
    return sum(prob(self, y_i, w) for y_i in self.gamma.keys()) / gamma_len


def prob(self, w, y_i):
    if w + ' ' + y_i not in self.bigram_freq:
        return 0
    return self.bigram_freq[w + ' ' + y_i] / N


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


def important(self, words):
    best = ''
    best_score = 0.0
    for w in words:
        w_score = score(self, w)
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


def display(self):
    data = [[w, self.gamma[w], score(self, w), syllable_count(w), len(w)] for w in self.gamma.keys()]
    print(tabulate(data, headers = ['Word', 'Freq', 'Score', 'Syllables', 'Length']))
    print('\nMost important word is:', important(self, list(self.gamma.keys())))


def markov_chain(self, word_):
    sen = ''

    if word_ not in self.gamma.keys():
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
        for s in self.gamma.keys():
            val = prob(self, word, s)
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
