import csv 

seed_chars = "xqjkwz"
hr_chars = "etaisrno"

# load bigram_count.csv form data folder
# disregard the first row
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
    
    for hr_char in hr_chars: 
        
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
    
    if char1 in seed_chars and char2 in hr_chars:
        best_placements.append(char1 + char2)
        
        seed_chars = seed_chars.replace(char1, "")
        seed_chars = seed_chars.replace(char2, "")
        
        hr_chars = hr_chars.replace(char2, "")
        hr_chars = hr_chars.replace(char1, "")
    
print(best_placements)

# dump into a csv file
with open("../data/best_placement.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["seed_char", "home_row_char", "frequency"])
    for seed_char, freq in sorted_best_placement.items():
        writer.writerow([seed_char[0], seed_char[1], freq])
                
                