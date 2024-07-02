import csv

bigram_count = {}

# read bigram and count
with open("../data/bigram_count.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        bigram_count[row["key"]] = int(row["value"])

# alpha = "abcdefghijklmnopqrstuvwxyz"
alpha = "etaisrno"

alpha_bigram_score = {}

for a in alpha:
    
    # for each bigram that contains a, add score to abs
    
    score = 0
    
    for bigram in bigram_count:
        if bigram.find(a) != -1:
            score += bigram_count[bigram]
    
    alpha_bigram_score[a] = score

# sort in DECENDING order
sorted_alpha_bigram_score = sorted(alpha_bigram_score.items(), key=lambda x: x[1], reverse=False)

for alpha, score in sorted_alpha_bigram_score:
    print(f"{alpha}: {score}")
