import csv
from itertools import permutations

alpha = "abcdefghijklmnopqrstuvwxyz"

bigram_count = {}

# read bigram and count
with open("../data/bigram_count.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        bigram_count[row["key"]] = int(row["value"])
        
char_bigram_score = {}

print(bigram_count)

for a in alpha:
    for b in alpha:
        if a == b:
            continue
        
        score = 0
        
        possible_bigrams = permutations([a, b], 2)
        
        for possible_bigram in possible_bigrams:
            possible_bigram = "".join(possible_bigram)
            if possible_bigram in bigram_count:
                score += bigram_count[possible_bigram]
        
        if a not in char_bigram_score:
            char_bigram_score[a] = 0
            
        print(score)
        
        char_bigram_score[a] += score
        
# sort in ascending order
sorted_char_bigram_score = sorted(char_bigram_score.items(), key=lambda x: x[1], reverse=True)

for char, score in sorted_char_bigram_score:
    print(f"{char}: {score}")
        
