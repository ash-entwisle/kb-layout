import csv

bigram_num = 6
input_file = f"../data/n-bigram/n{bigram_num}_bigram_score.csv"
output_file = f"../data/n-bigram/n{bigram_num}_bigram_score_filtered.csv"
filter_value = 1.6

with open(input_file, "r") as input_f, open(output_file, "w") as output_f:
    reader = csv.reader(input_f)
    writer = csv.writer(output_f)
    
    next(reader)
    writer.writerow(["key", "value"])
    
    for row in reader:
        key = row[0]
        value = float(row[1])
        if value > filter_value:
            continue

        writer.writerow([key, value])
