import csv

gamma = {}
bigram_freq = {}
preds = {}
succs = {}

with open('School/Capstone/ngrams_words_3.txt', newline='') as lines:
    reader = csv.reader(lines, delimiter = '\t')
    for line in reader:
        line = ' '.join(line)
        line = line.lower().split(' ')
        #print(line[1:4])
        gamma[line[1]] = gamma.get(line[1], 0) + 1
        gamma[line[2]] = gamma.get(line[2], 0) + 1
        gamma[line[3]] = gamma.get(line[3], 0) + 1
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

#print(gamma)
print(bigram_freq)
#print(preds)
#print(succs)