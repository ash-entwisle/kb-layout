import csv
from itertools import permutations


nbg_to_calc = 2
num_of_perms = 3
filter_value = 1.6

nbg_file = f"../data/n-bigram/n{nbg_to_calc}_bigram_score_filtered.csv"
out_file = f"../data/pregen/{num_of_perms}n{nbg_to_calc}_bigram_score_filtered.csv"

nbg = {}

with open(nbg_file, "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        nbg[row[0]] = float(row[1])


# get perms of just nbg strings
nbg_strings = list(nbg.keys())
perms = permutations(nbg_strings, num_of_perms)
perms_filtered = []

# remove all reversed perms (ab-cd, cd-ab)
for perm in perms:

    # check if any combination of the perm is already in perms_filtered
    perm_perms = permutations(perm, num_of_perms)
    to_add = True
    
    print(f"{perm}: {list(perm_perms)}")

    for p in perm_perms:
        if p in perms_filtered:
            to_add = False
            break
    
    if to_add:
        perms_filtered.append(perm)
    



with open(out_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["key", "value"])
    
    for perm in perms_filtered:
        
        # check if all letters are unique
        if len(set("".join(perm))) != num_of_perms * nbg_to_calc:
            continue
        

        
        score = 0
        for ng in perm:
            score += nbg[ng]
        
        if score > filter_value:
            continue 
            
        writer.writerow(["-".join(perm), score])
