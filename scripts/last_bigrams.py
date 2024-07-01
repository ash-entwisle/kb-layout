import csv
from itertools import permutations

alpha = "sirn"

bigram_count = {}

# read bigram and count
with open("../data/bigram_count.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        bigram_count[row["key"]] = int(row["value"][:-2])

char_bigram_score = {}

perms = permutations(alpha, 2)

for perm in perms:
    a, b = perm
    score = 0

    possible_bigrams = [
        a + b,
        b + a
    ]
    
    # if either bigram is in the bigram count, add it to the score
    for possible_bigram in possible_bigrams:
        if possible_bigram in bigram_count:
            score += bigram_count[possible_bigram]
            break

    if a not in char_bigram_score:
        char_bigram_score[a+b] = 0

    char_bigram_score[a+b] += score
    
    # if reverse bigram is presnt, remove it
    if b+a in char_bigram_score:
        del char_bigram_score[b+a]

# sort in ascending order
sorted_char_bigram_score = sorted(char_bigram_score.items(), key=lambda x: x[1], reverse=False)

burned_chars = ""


for char, score in sorted_char_bigram_score:
    if char[0] in burned_chars or char[1] in burned_chars:
        continue
    
    print(f"{char}: {score}")
    
    burned_chars += char[0]
    burned_chars += char[1]
    
    

