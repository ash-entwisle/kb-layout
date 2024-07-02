import csv

bigram_count = {}
alphabet = "abcdefghijklmnopqrstuvwxyz"

# read bigram and count 
with open("../data/bigram_count.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        bigram_count[row["key"]] = int(row["value"])

# sort bigram by count
sorted_bigram = sorted(bigram_count.items(), key=lambda x: x[1], reverse=True)

quadgrams = {}

for a in alphabet:
    for b in alphabet:
        for c in alphabet:
            for d in alphabet:
                
                
                get_out = False
                # if a quadram exists that contains either a,b,c,d, skip it
                for quadgram in quadgrams:
                    # if a quadgram contains a, b, c and d, skip it
                    if quadgram.find(a) != -1 and quadgram.find(b) != -1 and quadgram.find(c) != -1 and quadgram.find(d) != -1:
                        get_out = True
                        break
                
                if set([a,b,c,d]).__len__() != 4:
                    get_out = True
                else:
                    print(a,b,c,d)
                
                if get_out:
                    continue
                
                count = 0
                
                possible_bigrams = [
                    a + b, b + a, a + c, c + a,
                    a + d, d + a, b + c, c + b,
                    b + d, d + b, c + d, d + c
                ]
                
                for possible_bigram in possible_bigrams:
                    if possible_bigram in bigram_count:
                        count += bigram_count[possible_bigram]
                    
                quadgram = a + b + c + d
                quadgrams[quadgram] = count                       


# sort quadgram by count
sorted_quadgram = sorted(quadgrams.items(), key=lambda x: x[1], reverse=True)

# write quadgram to file
with open("../data/quadgrams.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["key", "value"])
    for quadgram, count in sorted_quadgram:
        writer.writerow([quadgram, count])

# for each quadgram, print it, burn the characters, repeat until the end
for quadgram, count in sorted_quadgram:
    print(quadgram)
    alphabet = alphabet.replace(quadgram[0], "")
    alphabet = alphabet.replace(quadgram[1], "")
    alphabet = alphabet.replace(quadgram[2], "")
    alphabet = alphabet.replace(quadgram[3], "")
    
    if len(alphabet) == 0:
        break
    
        