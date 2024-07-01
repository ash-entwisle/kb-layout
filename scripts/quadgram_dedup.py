import csv

# load quadgram data
quadgrams = {}

with open("../data/quadgrams.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        # print row indices
        quadgrams[row[0]] = int(row[1])
        
        # quadgrams[row["key"]] = int(row["value"])

char_freq = {}

with open("../data/char_alpha_count.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        char_freq[row[0]] = int(row[1])

# for each quadgram check if it has 4 unique characters
# if it does, add it to the list of valid quadgrams

valid_quadgrams = {}

for quadgram in quadgrams:
    if len(set(quadgram)) == 4:
        
        char1 = quadgram[0]
        char2 = quadgram[1]
        char3 = quadgram[2]
        char4 = quadgram[3]
        
        char_freq1 = char_freq[char1]
        char_freq2 = char_freq[char2]
        char_freq3 = char_freq[char3]
        char_freq4 = char_freq[char4]
        
        valid_quadgrams[quadgram] = quadgrams[quadgram] * (char_freq1 + char_freq2 + char_freq3 + char_freq4)

# sort quadgrams in descending order
sorted_quadgrams = sorted(valid_quadgrams.items(), key=lambda x: x[1], reverse=False)

burned_chars = set()
ignored_chars = "zkxwjqetaisr"
must_include = "no"

for char in ignored_chars:
    burned_chars.add(char)

for quadgram, count in sorted_quadgrams:
    
    go_again = False
    
    for char in quadgram:
        if char in burned_chars:
            go_again = True
            continue
    
    if go_again:
        continue
    
    # quadgram must have one character in must_include
    # if not, skip
    includes = False
    for char in must_include:
        if char in quadgram:
            includes = not includes

    if not includes:
        continue

    print(f"{quadgram}: {count}")
    
    for char in quadgram:
        burned_chars.add(char)
