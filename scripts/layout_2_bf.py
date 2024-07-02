import csv

from itertools import permutations

alpha = "abcdefghijklmnopqrstuvwxyz"
home_row_chars = "etaisrno"

n3_bigram_score = {}

with open("../data/n-bigram/n3_bigram_score.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n3_bigram_score[row["key"]] = float(row["value"])

# reverse n3_bigram_score
n3_bigram_score = {k: v for k, v in sorted(n3_bigram_score.items(), key=lambda item: item[1], reverse=True)}

n4_bigram_score = {}

with open("../data/n-bigram/n4_bigram_score.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n4_bigram_score[row["key"]] = float(row["value"])

# reverse n6_bigram_score
n4_bigram_score = {k: v for k, v in sorted(n4_bigram_score.items(), key=lambda item: item[1], reverse=True)}


best_score = 2
min_cap = 0.25
best_g1 = ""
best_g2 = ""
best_g3 = ""
best_g4 = ""
best_g5 = ""
best_g6 = ""
best_g7 = ""
best_g8 = ""

for g1 in n4_bigram_score:
    
    g1_score = n4_bigram_score[g1]
    if g1_score > min_cap or g1_score > best_score:
        continue
    
    if g1_score > best_score:
        continue
    
    if not any(c in home_row_chars for c in g1):
        continue
    
    for g2 in n4_bigram_score:
        
        to_continue = False
        for c in g2:
            if c in g1:
                to_continue = True
                break
            
        if not any(c in home_row_chars for c in g2):
            continue
        
        if to_continue:
            continue
        
        g2_score = n4_bigram_score[g2]
        if g2_score > min_cap or g2_score > best_score:
            continue
        
        if g1_score > best_score:
            break
        
        for g3 in n3_bigram_score:
                
            to_continue = False
            for c in g3:
                if c in g1 or c in g2:
                    to_continue = True
                    break
                
            if not any(c in home_row_chars for c in g3):
                continue
            
            if to_continue:
                continue
            
            g3_score = n3_bigram_score[g3]
            if g3_score > min_cap:
                continue
            
            if g3_score > best_score:
                continue
            
            if g1_score + g2_score > best_score:
                break
            
            for g4 in n3_bigram_score:
                
                to_continue = False
                for c in g4:
                    if c in g1 or c in g2 or c in g3:
                        to_continue = True
                        break
                    
                if not any(c in home_row_chars for c in g4):
                    continue
                
                if to_continue:
                    continue
                
                g4_score = n3_bigram_score[g4]
                if g4_score > min_cap:
                    continue
                
                if g4_score > best_score:
                    continue
                
                if g1_score + g2_score + g3_score > best_score:
                    break   
                
                for g5 in n3_bigram_score:
                    
                    to_continue = False
                    for c in g5:
                        if c in g1 or c in g2 or c in g3 or c in g4:
                            to_continue = True
                            break
                        
                    if not any(c in home_row_chars for c in g5):
                        continue
                    
                    if to_continue:
                        continue
                    
                    g5_score = n3_bigram_score[g5]
                    if g5_score > min_cap or g5_score > best_score:
                        continue
                    
                    if g1_score + g2_score + g3_score + g4_score > best_score:
                        break
                    
                    for g6 in n3_bigram_score:
                        
                        to_continue = False
                        for c in g6:
                            if c in g1 or c in g2 or c in g3 or c in g4 or c in g5:
                                to_continue = True
                                break
                            
                        if not any(c in home_row_chars for c in g6):
                            continue
                        
                        if to_continue:
                            continue
                        
                        g6_score = n3_bigram_score[g6]
                        if g6_score > min_cap:
                            continue
                        
                        if g6_score > best_score:
                            continue
                        
                        if g1_score + g2_score + g3_score + g4_score + g5_score > best_score:
                            break
                        
                        for g7 in n3_bigram_score:
                            
                            to_continue = False
                            for c in g7:
                                if c in g1 or c in g2 or c in g3 or c in g4 or c in g5 or c in g6:
                                    to_continue = True
                                    break
                                
                            if not any(c in home_row_chars for c in g7):
                                continue
                            
                            if to_continue:
                                continue
                            
                            g7_score = n3_bigram_score[g7]
                            if g7_score > min_cap:
                                continue
                            
                            if g7_score > best_score:
                                continue
                            
                            if g1_score + g2_score + g3_score + g4_score + g5_score + g6_score > best_score:
                                break
                            
                            for g8 in n3_bigram_score:
                                
                                
                                to_continue = False
                                for c in g8:
                                    if c in g1 or c in g2 or c in g3 or c in g4 or c in g5 or c in g6 or c in g7:
                                        to_continue = True
                                        break
                                
                                if to_continue:
                                    continue
                                
                                g8_score = n3_bigram_score[g8]
                                if g8_score > min_cap:
                                    continue
                                
                                print(f"{g1} {g2} {g3} {g4} {g5} {g6} {g7} {g8}")
                                print(f"{g1_score + g2_score + g3_score + g4_score + g5_score + g6_score + g7_score + g8_score}")
                                
                                if g8_score > best_score:
                                    continue
                                
                                score = g1_score + g2_score + g3_score + g4_score + g5_score + g6_score + g7_score + g8_score
                                if score < best_score:
                                    best_score = score
                                    best_g1 = g1
                                    best_g2 = g2
                                    best_g3 = g3
                                    best_g4 = g4
                                    best_g5 = g5
                                    best_g6 = g6
                                    best_g7 = g7
                                    best_g8 = g8
                                    
                                    print(f"Best Score: {best_score}")  
                                    print(f"{best_g1} {best_g2} {best_g3} {best_g4} {best_g5} {best_g6} {best_g7} {best_g8}")
                    