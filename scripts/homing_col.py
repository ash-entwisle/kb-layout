import csv

remaining_chars = "bcdfghlmpuvy" # todo, finalise this
seed_chars = "ai"

bigram_count = {}

with open("../data/bigram_count.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        bigram_count[row[0]] = int(row[1])
        
placements = {}

for seed_char in seed_chars:
        
    best_freq = 0
    best_char = ""
    
    for hr_char in remaining_chars: 
        
        bigram_left = hr_char + seed_char
        bigram_right = seed_char + hr_char
        
        if bigram_left in bigram_count:
            freq = bigram_count[bigram_left]
            
            if freq < best_freq or best_freq == 0:
                best_freq = freq
                best_char = hr_char
            
        elif bigram_right in bigram_count:
            freq = bigram_count[bigram_right]
            
            if freq < best_freq or best_freq == 0:
                best_freq = freq
                best_char = hr_char
            
    placements[seed_char + best_char] = best_freq

# sort the dictionary by value in ascending order
sorted_best_placement = dict(sorted(placements.items(), key=lambda item: item[1]))
best_placements = []

for best_placement, freq in sorted_best_placement.items():
    char1 = best_placement[0]
    char2 = best_placement[1]
    
    if char1 in seed_chars and char2 in remaining_chars:
        best_placements.append(char1 + char2)
        
        seed_chars = seed_chars.replace(char1, "")
        seed_chars = seed_chars.replace(char2, "")
        
        remaining_chars = remaining_chars.replace(char2, "")
        remaining_chars = remaining_chars.replace(char1, "")
        

print(best_placements)
print(remaining_chars)
