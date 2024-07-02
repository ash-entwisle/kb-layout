import csv

from itertools import permutations


colemak = ["zaq", "xrw", "csf", "dtpvgb", "", "", "kmjhnl", "eu", "iy", "o"]
isrt = ["qiy", "vsc", "wrl", "dtmjgk", "", "", "bpzhnf", "eu", "a", "ox"]
isrt_mod = []
qwerty = ["qaz", "wsx", "edc", "rfvtgb", "", "", "yhnujm", "ik", "ol", "p"]

mine = ["xsm", "krl", "ztb", "nfyh", "", "", "vuog", "qec", "wip", "jad"]
mine_v2 = ["qaz", "xcw", "udy", "ptmjvb", "", "", "kfgloh", "is", "rn", "e"]


layouts = {
    "colemak": colemak,
    "isrt": isrt,
    "qwerty": qwerty,
    "mine": mine,
    "mine_v2": mine_v2
}

def main():

    # load bigram data
    bigram_count = {}
    
    with open("../data/bigram_count.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            bigram_count[row["key"]] = int(row["value"])
            
    bigram_sum = sum(bigram_count.values())
    
    # for each value in bigram, change it to the percentage to 2 decimal places
    for bigram in bigram_count:
        bigram_count[bigram] = round(bigram_count[bigram] / bigram_sum * 100, 2)
        
            
    # for each layout, for each column, calculate the bigram score
    for layout in layouts:
        
        print(f"Layout: {layout}")
        
        total = 0
        
        for i in range(len(layouts[layout])):
            column = layouts[layout][i]
            
            score = 0
            
            for bigram in permutations(column, 2):
                bigram = "".join(bigram)
                if bigram in bigram_count:
                    score += bigram_count[bigram]
            
            print(f"- Finger {i + 1}: {round(score, 2)}")
            total += score
        
        print(f"%SFB: {round(total, 2)}")
        print()


if __name__ == "__main__":
    main()       
