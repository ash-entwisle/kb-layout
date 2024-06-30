import csv

# load bigram_count.csv form data folder
# disregard the first row
bigram_count = {}

with open("../data/bigram_count.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        bigram_count[row[0]] = int(row[1])
        
alphas = "abcdefghijklmnopqrstuvwxyz"

alpha_freq_in_bigrams = {}

for alpha in alphas:
    for pair in alphas:
        
        bigram_left = alpha + pair
        bigram_right = pair + alpha
        
        if bigram_left in bigram_count:
            freq = bigram_count[bigram_left]
            
            if alpha not in alpha_freq_in_bigrams:
                alpha_freq_in_bigrams[alpha] = freq
            else:
                alpha_freq_in_bigrams[alpha] += freq
            
        elif bigram_right in bigram_count:
            freq = bigram_count[bigram_right]
            
            if alpha not in alpha_freq_in_bigrams:
                alpha_freq_in_bigrams[alpha] = freq
            else:
                alpha_freq_in_bigrams[alpha] += freq
                

# sort the dictionary by value in ascending order
sorted_alpha_freq_in_bigrams = dict(sorted(alpha_freq_in_bigrams.items(), key=lambda item: item[1]))

# dump into a csv file
with open("../data/least_frequent_alpha.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["alpha", "frequency"])
    for alpha, freq in sorted_alpha_freq_in_bigrams.items():
        writer.writerow([alpha, freq])
                
        