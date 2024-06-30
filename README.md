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


