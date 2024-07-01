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
     0   1   2   3   4       5   6   7   8   9   
   +---+---+---+---+---+   +---+---+---+---+---+
a  |   |   |   |   |   |   |   |   |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
b  |   |   |   |   |   |   |   |   |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
c  |   |   |   | * | * |   | * | * |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
d              | * | * |   | * | * |
               +---+---+   +---+---+

```

##### Row-C Characters

To place the characters in row-c, I will find the characters that are used the least in bigrams. 
This aims to reduce the frequency of same-finger bigrams as well as moving more common characters away from the bottom row.
The 6 least-used characters in bigrams are; `zjkqwx`, Placing them on the keymap gives us something like this:

```txt
     0   1   2   3   4       5   6   7   8   9   
   +---+---+---+---+---+   +---+---+---+---+---+
a  |   |   |   |   |   |   |   |   |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
b  |   |   |   |   |   |   |   |   |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
c  | z | k | x | * | * |   | * | * | w | j | q | 
   +---+---+---+---+---+   +---+---+---+---+---+
d              | * | * |   | * | * |
               +---+---+   +---+---+

```

##### Home row, col 3 and 6

The home row tiles (excl col 4 and 6) should be populated with the most frequent characters, 
these being; `etaisrno`. 
To find the most optimal characters to place in columns 3 and 6, I need to find the characters
with the lowest bigram frequency. 
This is because the index fingers (responsible for rows 3-6) are responsible for more keys than the other fingers.
the 2 characters out of the most frequenc characters with the lowest bigram frequency are `o` and `n`, 
this gives us the following layout:

```txt
     0   1   2   3   4       5   6   7   8   9   
   +---+---+---+---+---+   +---+---+---+---+---+
a  |   |   |   |   |   |   |   |   |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
b  |   |   |   | o |   |   |   | n |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
c  | z | k | x | * | * |   | * | * | w | j | q | 
   +---+---+---+---+---+   +---+---+---+---+---+
d              | * | * |   | * | * |
               +---+---+   +---+---+

```



##### Index-Finger Quadgrams

So far, we have used the keys; `zkxwjq`, we also have the following keys reserved for the home row; `etaisrno`.
The quadgram must also inlude `o` and `n`. 
After removing modifiers, the index fingers are responsible for 4 keys each.
To find the optimal placement of the alpha characters on the primary layer,
I will calculate a score for each quadgram of alpha characters 
by combining the frequency of each possible bigram. 
I then weighted the score for each quadgram agains the sum of each letter frequency
to get a score for each quadgram.
I then took the two highest scoring quadgrams for each index finger and placed them on the keyboard.
This gave us the quadgrams `fhny` and `gouv`. 

When placing these quadgrams, the most frequent character is placed under the index finger (homing character).
From there, for each pair, I need to find the two most optimal bigrams, this is to reduce vertical movement.
To do this, I just compared the possible bigrams of the homing character, 
placed the highest closest to the middle of the keyboard, the lowest above the highest. 
and the last one above the homing character.

```txt
     0   1   2   3   4       5   6   7   8   9   
   +---+---+---+---+---+   +---+---+---+---+---+
a  |   |   |   | f | h |   | u | g |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
b  |   |   |   | n | y |   | v | o |   |   |   |
   +---+---+---+---+---+   +---+---+---+---+---+
c  | z | k | x | * | * |   | * | * | w | j | q | 
   +---+---+---+---+---+   +---+---+---+---+---+
d              | * | * |   | * | * |
               +---+---+   +---+---+

```

##### Optimal Tripple Bi-grams

to fill in the remaining columns, I need to find combinations of 3 characters that have the lowest bigram frequency.
These will then be placed in the remaining columns.
So far, ive consumed the following characters; `zkxwjqfhnygovu`.
Now, I need to find the 3 characters with the lowest bigram frequency 
while requiring they contain one of the characters from row c (`zkxwjq`). 
I also added a check to make sure each tripple bigram contains at least one home-row character (`etaisr`).


```txt
     0   1   2   3   4       5   6   7   8   9   
   +---+---+---+---+---+   +---+---+---+---+---+
a  | m | l | b | f | h |   | u | g | c | p | d | 
   +---+---+---+---+---+   +---+---+---+---+---+
b  | s | r | t | n | y |   | v | o | e | i | a |
   +---+---+---+---+---+   +---+---+---+---+---+
c  | x | k | z | * | * |   | * | * | q | w | j | 
   +---+---+---+---+---+   +---+---+---+---+---+
d              | * | * |   | * | * |
               +---+---+   +---+---+

```

> Alr... after analysing the layout, its not as efficient as I thought it would be, 
> however i have learned how colemak and isrt optimise sfb's