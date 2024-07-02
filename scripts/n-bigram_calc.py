import csv 

from itertools import permutations

bigram_count = {}

with open("../data/bigram_count.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        bigram_count[row["key"]] = int(row["value"])


# change value to %

bigram_sum = sum(bigram_count.values())

for bigram in bigram_count:
    bigram_count[bigram] = bigram_count[bigram] / bigram_sum * 100 # %bigram


alpha = "abcdefghijklmnopqrstuvwxyz"

        
def n_bigram_score_calc(n: int):
    possible_n_bigram = permutations(alpha, n)
    possible_n_bigram = [n_bigram for n_bigram in possible_n_bigram if len(set(n_bigram)) == n]
    # possible_n_bigram = [bigram for bigram in possible_n_bigram if bigram == "".join(sorted(bigram))]

    
    n_bigrams = set()
    
    for c in possible_n_bigram:
        bigram_normal = "".join(sorted(c))
        n_bigrams.add(bigram_normal)
    
    print(n_bigrams.__len__())    
        




    n_bigram_score = {}


    for n_bigram in n_bigrams:

        perm = permutations(n_bigram, 2)
        
        score = 0
        
        for p in perm:
            bigram = "".join(p)
            
            
            if bigram in bigram_count:
                score += bigram_count[bigram]
                
        n_bigram_score[n_bigram] = score

    sorted_n_bigram_score = sorted(n_bigram_score.items(), key=lambda x: x[1], reverse=False)

    with open(f"../data/n-bigram/n{str(n)}_bigram_score.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["key", "value"])
        for key, value in sorted_n_bigram_score:
            writer.writerow([key, value])

if __name__ == "__main__":
    
    n_bigram_score_calc(2)    
    n_bigram_score_calc(3)
    n_bigram_score_calc(4)
    n_bigram_score_calc(5)
    n_bigram_score_calc(6)