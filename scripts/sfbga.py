import csv

from itertools import permutations


colemak = [
    "zaq",
    "xrw",
    "csf",
    "dtpvgb",
    "",
    "",
    "kmjhnl",
    "eu",
    "iy",
    "o"
]

isrt = [
    "qiy",
    "vsc",
    "wrl",
    "dtm",
    "jgk",
    "",
    "",
    "bpz",
    "hnf",
    "eu",
    "a",
    "ox"
]

mine = [
    "xsm",
    "krl",
    "ztb",
    "nfyh",
    "",
    "",
    "vuog",
    "qec",
    "wip",
    "jad"
]


layouts = {
    "colemak": colemak,
    "isrt": isrt,
    "mine": mine
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
        
        print()
        print(f"SFB/finger: {round(total, 2)}")
        
        
if __name__ == "__main__":
    main()       
        
            
