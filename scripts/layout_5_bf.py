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
# n3_bigram_score = {k: v for k, v in sorted(n3_bigram_score.items(), key=lambda item: item[1], reverse=True)}

n6_bigram_score = {}

with open("../data/n-bigram/n6_bigram_score.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n6_bigram_score[row["key"]] = float(row["value"])

# reverse n6_bigram_score
# n6_bigram_score = {k: v for k, v in sorted(n6_bigram_score.items(), key=lambda item: item[1], reverse=True)}


best_score = 1.75 # isrt is 2.88, ive gotten as low as 1.66 in testing, just to speed stuff up lol
min_cap = 0.5
best_g1 = ""
best_g2 = ""
best_g3 = ""
best_g4 = ""
best_g5 = ""
best_g6 = ""

for g1 in n6_bigram_score:

    g1_score = n6_bigram_score[g1]
    if g1_score > min_cap or g1_score > best_score:
        continue

    if g1_score > best_score:
        continue

    if not any(c in home_row_chars for c in g1):
        continue

    for g2 in n6_bigram_score:

        if g1_score > best_score:
            break

        to_continue = False
        for c in g2:
            if c in g1:
                to_continue = True
                break

        if not any(c in home_row_chars for c in g2):
            continue

        if to_continue:
            continue

        g2_score = n6_bigram_score[g2]
        if g2_score > min_cap or g2_score > best_score:
            continue


        for g3 in n3_bigram_score:

            if g1_score + g2_score > best_score:
                break

            to_continue = False
            for c in g3:
                if c in g1 or c in g2:
                    to_continue = True
                    break

            if to_continue:
                continue

            g3_score = n3_bigram_score[g3]
            if g3_score > min_cap or g3_score > best_score:
                continue


            for g4 in n3_bigram_score:

                if g1_score + g2_score + g3_score > best_score:
                    break

                to_continue = False
                for c in g4:
                    if c in g1 or c in g2 or c in g3:
                        to_continue = True
                        break

                if to_continue:
                    continue

                g4_score = n3_bigram_score[g4]
                if g4_score > min_cap or g4_score > best_score:
                    continue

                for g5 in n3_bigram_score:

                    to_continue = False
                    for c in g5:
                        if c in g1 or c in g2 or c in g3 or c in g4:
                            to_continue = True
                            break

                    if to_continue:
                        continue

                    g5_score = n3_bigram_score[g5]
                    if g5_score > min_cap or g5_score > best_score:
                        continue

                    if g1_score + g2_score + g3_score + g4_score > best_score:
                        break

                    for g6 in n3_bigram_score:

                        if g1_score + g2_score + g3_score + g4_score + g5_score > best_score:
                            break

                        to_continue = False
                        for c in g6:
                            if c in g1 or c in g2 or c in g3 or c in g4 or c in g5:
                                to_continue = True
                                break

                        if to_continue:
                            continue

                        g6_score = n3_bigram_score[g6]
                        if g6_score > min_cap or g6_score > best_score:
                            continue

                        score = g1_score + g2_score + g3_score + g4_score + g5_score + g6_score
                        if score < best_score:
                            best_score = score
                            best_g1 = g1
                            best_g2 = g2
                            best_g3 = g3
                            best_g4 = g4
                            best_g5 = g5
                            best_g6 = g6

                            print(f"Best Score: {best_score}")  
                            print(f"{best_g1} {best_g2} {best_g3} {best_g4} {best_g5} {best_g6}")
