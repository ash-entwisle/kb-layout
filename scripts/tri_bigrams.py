import csv
from itertools import permutations

bigram_count = {}

# read bigram and count
with open("../data/bigram_count.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        bigram_count[row["key"]] = int(row["value"])

alpha_freq = {}

with open("../data/char_alpha_count.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        alpha_freq[row["key"]] = int(row["value"])


# sort bigram by count
sorted_bigram = sorted(bigram_count.items(), key=lambda x: x[1], reverse=True)

used_chars = "e"
alphabet = "abcdefghijklmnopqrstuvwxyz"
# required_chars = "zkxwjq"
# required_hr = "etaisr"

for chars in used_chars:
    alphabet = alphabet.replace(chars, "")

# for chars in required_chars:
#     alphabet = alphabet.replace(chars, "")
    
# for chars in required_hr:
#     alphabet = alphabet.replace(chars, "")

tri_bigram = {}

for a in alphabet:
    for b in alphabet:
        for c in alphabet:
            
            if a == b or a == c or b == c:
                continue
            
            possible_tri_bigrams = permutations([a, b, c], 3)
            
            to_break = False
            
            for possible_tri_bigram in possible_tri_bigrams:
                if possible_tri_bigram in tri_bigram:
                    to_break = True
                    break
            
            if to_break:
                continue
            
            possible_bigrams = permutations([a, b, c], 2)
            
            for possible_bigram in possible_bigrams:
                possible_bigram = "".join(possible_bigram)
                
                if possible_bigram in bigram_count:
                    if a not in tri_bigram:
                        tri_bigram[a + b + c] = 0

                    tri_bigram[a + b + c] += bigram_count[possible_bigram]

# sort tri_bigram by count, reverse
sorted_tri_bigram = sorted(tri_bigram.items(), key=lambda x: x[1], reverse=False)

burned_chars = set()

for tri_bigram, count in sorted_tri_bigram:

    burned = False
    for char in tri_bigram:
        if char in burned_chars:
            burned = True
            continue
    
    if not burned:
        
        char1 = tri_bigram[0]
        char2 = tri_bigram[1]
        char3 = tri_bigram[2]
        
        print(f"{tri_bigram}: {count} {alpha_freq[char1] + alpha_freq[char2] + alpha_freq[char3]}")
        for char in tri_bigram:
            burned_chars.add(char)

# find all characters in alphabet that arent in burned_chars
# print them
for char in alphabet:
    if char not in burned_chars:
        print(char)