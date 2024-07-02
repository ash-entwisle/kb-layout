import csv

# bigram_count = {}

# # read bigram and count
# with open("../data/bigram_count.csv") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         bigram_count[row["key"]] = int(row["value"])
        
# for bigram in bigram_count:

#     value = bigram_count[bigram]
#     bigram_count[bigram] = int(value)/2
    
# with open("../data/bigram_count.csv", "w") as f:
#     writer = csv.DictWriter(f, fieldnames=["key", "value"])
#     writer.writeheader()
#     for bigram, value in bigram_count.items():
#         writer.writerow({"key": bigram, "value": value})