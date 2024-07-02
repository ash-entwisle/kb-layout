import csv

quadrgams_borked = {}

with open("../data/quadgrams.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for quadgram, count in reader:
        quadrgams_borked[quadgram] = count

# for each key
# add it to list

quadgrams = {}

for quadgram in quadrgams_borked:
    quadgrams[quadgram] = 0


bigram_count = {}

with open("../data/bigram_count.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        bigram_count[row["key"]] = int(row["value"])

# sort bigram by count
sorted_bigram = sorted(bigram_count.items(), key=lambda x: x[1], reverse=True)

# for each quadgram, get every possible bigram combination
# if a bigram is in the bigram count, add it to the count of the quadgram

for quadgram in quadgrams:
    
    count = 0
    a = quadgram[0]
    b = quadgram[1]
    c = quadgram[2]
    d = quadgram[3]
    
    possible_bigrams = [
        a + b,
        b + a,
        a + c,
        c + a,
        a + d,
        d + a,
        b + c,
        c + b,
        b + d,
        d + b,
        c + d,
        d + c
    ]
    
    for possible_bigram in possible_bigrams:
        if possible_bigram in bigram_count:
            count += bigram_count[possible_bigram]
            
    quadgrams[quadgram] = count
    
    
# sort quadgrams by count in ascending order
sorted_quadgrams = sorted(quadgrams.items(), key=lambda x: x[1], reverse=True)

# overwrite the quadgrams file with the valid quadgrams
with open("../data/quadgrams.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["key", "value"])
    for quadgram, count in sorted_quadgrams:
        writer.writerow([quadgram, count])
    