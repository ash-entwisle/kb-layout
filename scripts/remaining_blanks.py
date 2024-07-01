import csv

remaining_chars = "bcdfghlmpuvy" 
seed_bigrams = ["rz", "sx", "ek", "tw", "qo", "nj"]

bigram_count = {}

with open("../data/bigram_count.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        bigram_count[row[0]] = int(row[1])
        
placements = {}

for seed_bigram in seed_bigrams:
        
    for hr_char in remaining_chars:
        
        char1 = seed_bigram[0]
        char2 = seed_bigram[1]
        char3 = hr_char
        
        bg_freq = 0
        
        # find bigram that contains char1 and char2
        bigram_left = char1 + char2
        bigram_right = char2 + char1
        
        if bigram_left in bigram_count:
            bg_freq += bigram_count[bigram_left]
        elif bigram_right in bigram_count:
            bg_freq += bigram_count[bigram_right]
            
        # find bigram that contains char2 and char3
        bigram_left = char2 + char3
        bigram_right = char3 + char2
        
        if bigram_left in bigram_count:
            bg_freq += bigram_count[bigram_left]
        elif bigram_right in bigram_count:
            bg_freq += bigram_count[bigram_right]
            
        # find bigram that contains char1 and char3
        bigram_left = char1 + char3
        bigram_right = char3 + char1
        
        if bigram_left in bigram_count:
            bg_freq += bigram_count[bigram_left]
        elif bigram_right in bigram_count:
            bg_freq += bigram_count[bigram_right]
            
        placements[seed_bigram + char3] = bg_freq

# sort the dictionary by value in ascending order
sorted_best_placement = dict(sorted(placements.items(), key=lambda item: item[1]))

best_placements = []
burned_chars = ""

for best_placement, freq in sorted_best_placement.items():
    char1 = best_placement[0]
    char2 = best_placement[1]
    char3 = best_placement[2]
    
    if char1 in burned_chars or char2 in burned_chars or char3 in burned_chars:
        continue
    
    best_placements.append(char1 + char2 + char3)
    
    burned_chars += char1
    burned_chars += char2
    burned_chars += char3
    
print(best_placements)

# write to tri_bigram_freqs

with open("../data/tri_bigram_freqs.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["seed_bigram", "frequency"])
    for seed_bigram, freq in sorted_best_placement.items():
        writer.writerow([seed_bigram, freq])
        