# kb-layout

> This is a work-in-progress project to create my own layout. This project is yet to be completed. 

## Introduction

This project aims to use ngram analysis to create a 34 key keyboard layout 
(e.g. [the ferris sweep]()) optimised for software development. 
To do this, I will analyse text from a corpus of source code 
against metrics such as same-finger bigrams, first-trigrams, and frequency of non-alpha characters 
to determine the optimal placement of each character on the keyboard.

## Methodology

### Corpus

The corpus used for this project comes from each top-100 repository listed in [this repo]().  
I recursively cloned each repository and extracted the text from all the files in the repository. 
The text was then cleaned, letters were converted to lowercase 
and all non-alpha characters were flattened to their unshifted form 
as per the US/ANSI Keyboard layout (e.g. `!` to `1`, `@` to `2`, `:` to `;` etc.). 

After this, all numeric characters were removed from the text 
as numbers will live on their own separate layer on the keyboard.
This data was then split into two separate files, 
one containing just the alpha characters and the other containing just the non-alpha characters.

#### List of Repositories

To get a list of repositories, I used the following script to scrape a list of md files 
from the top 100's repo mentioned earlier (this list can be found [here](./data/repos.txt)).

```python
import requests
import re

# MD files to scrape
md_files = [
    # see file for full list...
]

# For each md file, scrape it and add all github repos to a set
repos = set()

for md_file in md_files:
    response = requests.get(md_file)
    # response is in raw text
    text = response.text
    
    print(text)
    
    # find all github repo links https://github.com/username/repo
    matches = re.findall(r'https:\/\/github\.com\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+' , text)
    for match in matches:
        repos.add(match)

# Write all repos to a file
with open("../data/repos.txt", "w") as f:
    for repo in repos:
        f.write(repo + "\n")
        
print(f"Scraped {len(repos)} repos")
```

### Frequency Analysis

#### Alpha Bigrams

bigram analysis was performed using a modified version of [angr](https://github.com/ash-entwisle/angr). 
This is a tool I created to perform ngram analysis on text files. 
It was used to generate the bigram frequencies for the alpha characters 
from the only-alpha dataset to be used in placing the alpha characters on the primary layer of the keyboard.

This metric will be used to determine the placement of the alpha characters on the primary layer of the keyboard.
as well as what columns the characters should be placed in to avoid same-finger bigrams 
as much as possible to improve typing speed.

#### First Alpha Trigrams

First-trigram analysis was performed on the alpha characters from the only-alpha dataset.
This was used to determine the frequency of each first-trigram in the dataset.

This metric will be used alongside the bigram analysis 
to determine the placement of the alpha characters on the primary layer of the keyboard.
It aims to increase the score of letters near the start of words to get them closer to the home row
or closer to the middle of the keyboard. 


#### Non-Alpha Characters

Frequency analysis was performed on the non-alpha characters from the non-alpha dataset. 
This was used to determine the frequency of each non-alpha character in the dataset. 

This information was used to determine the placement of non-alpha combo keys on the keyboard.
Combo keys are keys that are pressed in combination with another key to produce a different output.
These are preferable over dedicated keys for non-alpha characters 
as they allow for more efficient use of space on the keyboard.



## Building the Layout

### Structure

The layout we are building is based around a 34 key layout such as the ferris sweep.
On the primary layer, we will have 26 alpha characters, a dedicated OS key, a dedicated number key, 
two layer keys (one for numbers and symbols, the other for misc stuff such as fn keys), 
and 4 other keys for other common actions (tab, enter, backspace, and esc).

Common symbols will live as combo keys on the primary layer and have a space on a dedicated symbol layer.
QMK has a default combo key for esc:~/\` which we will use for the esc key, 
that means we dont have to worry about placing ~/\` somewhere on the keyboard as a combo key.

The 4 common action keys will all live on separate columns to reduce same-finger bigrams.
This leaves us with 4 columns- each with 2 keys and 6 columns- each with 3 keys 
to place the remaining 26 alpha characters.

#### Key Placement

I've placed the 4 common action keys in the middle two columns for both the left and right hand.
This is because the index fingers are responsible for 6 keys each 
compared to the 3 keys other fingers are responsible for.
This gives us a layout that looks something like this 
(`*` represents all keys currently reserved for non-alpha characters):

```txt
+---+---+---+---+---+   +---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |   | 
+---+---+---+---+---+   +---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |   | 
+---+---+---+---+---+   +---+---+---+---+---+
|   |   |   | * | * |   | * | * |   |   |   | 
+---+---+---+---+---+   +---+---+---+---+---+
            | * | * |   | * | * |
            +---+---+   +---+---+

```

##### Least-frequent Alpha Characters

To further reduce the chance of same-finger bigrams, we will place the 6 least common, least frequent (in bi-grams)
alpha characters in the columns with 3 keys.
This gives us some breathing room to strategically place the remaining 20 alpha characters in the columns with 2 keys.

To find the least frequent, least common alpha characters, we will loop through each character in the alphabet 
and tally up its frequency for each bigram that it is a part of.
The 6 characters with the lowest frequency will be placed in the columns with 3 keys.
To achieve this, I used the following script:

```python
import csv

# load bigram_count.csv form data folder
# disregard the first row
bigram_count = {}

with open("../data/bigram_count.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        bigram_count[row[0]] = int(row[1])
        
alphas = "abcdefghijklmnopqrstuvwxyz"

alpha_freq_in_bigrams = {}

for alpha in alphas:
    for pair in alphas:
        
        bigram_left = alpha + pair
        bigram_right = pair + alpha
        
        if bigram_left in bigram_count:
            freq = bigram_count[bigram_left]
            
            if alpha not in alpha_freq_in_bigrams:
                alpha_freq_in_bigrams[alpha] = freq
            else:
                alpha_freq_in_bigrams[alpha] += freq
            
        elif bigram_right in bigram_count:
            freq = bigram_count[bigram_right]
            
            if alpha not in alpha_freq_in_bigrams:
                alpha_freq_in_bigrams[alpha] = freq
            else:
                alpha_freq_in_bigrams[alpha] += freq
                

# sort the dictionary by value in ascending order
sorted_alpha_freq_in_bigrams = dict(sorted(alpha_freq_in_bigrams.items(), key=lambda item: item[1]))

# dump into a csv file
with open("../data/least_frequent_alpha.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["alpha", "frequency"])
    for alpha, freq in sorted_alpha_freq_in_bigrams.items():
        writer.writerow([alpha, freq])
                
```

Running this, we got these results (truncated to 6, we dont need any more than that) :

```csv
alpha,  frequency
z,	    219036766
j,	    284698658
k,	    304223680
q,	    332261214
w,	    594309082
x,	    807949328
```

Placing these characters in the layout would give us a layout that looks like this. 
I moved the less frequent characters towards weaker fingers (ring and pinky) to try and reduce their usage.
(note, the `x` characters have been replaced with `*`):

```txt
+---+---+---+---+---+   +---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |   | 
+---+---+---+---+---+   +---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |   | 
+---+---+---+---+---+   +---+---+---+---+---+
| z | k | x | * | * |   | * | * | w | q | j | 
+---+---+---+---+---+   +---+---+---+---+---+
            | * | * |   | * | * |
            +---+---+   +---+---+

```

##### Placement of bi-grams in columns with 3 alpha keys

Now that we have placed the least frequent alpha characters, we can move on to placing the remaining 20 alpha characters.
For now, we'll just look at the 6 columns with 3 alpha keys.
For each of these columns, we will loop through each bi-gram 
and add the frequencies of every bigram of every combination of the 3 letters. 
The bigram with the lowest frequency will be placed in the column 
with the most frequent alpha character in the bigram placed on the home row. 









To find the ideal key combinations for each column, we need to group up 3 letters that are rarely used together.
This is because we want to avoid same-finger bigrams as much as possible.
To do this, we will loop through each possible tri-bigram and calculate the score for each one.
The score 