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

#### Non-Alpha Characters

Frequency analysis was performed on the non-alpha characters from the non-alpha dataset. 
This was used to determine the frequency of each non-alpha character in the dataset. 

This information was used to determine the placement of non-alpha combo keys on the keyboard.
Combo keys are keys that are pressed in combination with another key to produce a different output.
These are preferable over dedicated keys for non-alpha characters 
as they allow for more efficient use of space on the keyboard.



## Building the Layout

### Learning from Other Layouts

#### Pre-generating scores for tripple-bigrams, quad-bigrams, quint-bigrams and hex-bigrams

To speed up the process of generating scores for tripple-bigrams, quad-bigrams, quint-bigrams and hex-bigrams. 
These Scores come from groups of 3, 4, 5 and 6 characters and is a sum of the %chance of each bigram in the group.


#### Placement of Common Actions

A common thing amongst layouts such as ISRT, colemak and dvorak is how the common modifier keys are placed. 
When looking at what columns these are placed in, there are 4 common action keys, spread across 3 columns, 
one of which has two common action keys. Idk why this is good, but for some reason it works really well. 

#### Middle columns

Another thing that is common, mainly in colemak-dh and ISRT is the placement of less common characters in the middle column. 
This reduces same finger bigrams as the inner two columns on each hand are both responsible for 6 characters each.

#### Bigram Analysis of layouts 

I calculated the %sfbs for some common layouts such as colemak, isrt, qwerty 
and some custom ones made from previous attempts at this. 
It showed my previous attempts were better than qwerty but still worse than colemak and isrt.

| Layout    | %sfbs |
| --------- |-------|
| colemak   | 3.62% |
| isrt      | 2.88% |
| qwerty    | 7.88% |
| custom v1 | 4.72% |
| custom v2 | 6.59% |

However, some of these numbers start to change when looking at %sfb per finger. 
custom v1 had a better Finger 4 and finger 7 %sfb than colemak and isrt. 
Goal is, how do I find a way to translate that small success to a full layout? 

#### Playing around with the placement of common actions




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

### Key Placement

#### Layout 1

Using the common action key placements from other layouts, weve got a starting layout something like this
(`*` represents all keys currently reserved for non-alpha characters):

```txt
     0   1   2   3   4       5   6   7   8   9   
   +---+---+---+---+---+   +---+---+---+---+---+
a  |   |   |   |   |   |   |   |   |   |   | * | 
   +---+---+---+---+---+   +---+---+---+---+---+
b  |   |   |   |   |   |   |   |   |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
c  |   |   |   |   |   |   |   |   | * | * | * | 
   +---+---+---+---+---+   +---+---+---+---+---+
d              | * | * |   | * | * |
               +---+---+   +---+---+

```

We can further break this down by areas each finger uses. 
column 0, 1 and 2 are each managed by their own fingers. 
column 3 and 4 are managed by the same finger,
similar thing with columns 5 and 6. 
column 7, 8 and 9 each have their own fingers. 
This means we have 3 tripple-bigrams, 2 hex-bigrams, 2 bigrams and 1 remaining key.
For now, we can just ignore the single key and focus on the rest. 

After running my god awful code for a solid god knows how long, 
It settled on a layout that was most optimised for %SFBs.
After adjusting the common action keys, and making some other small adjustments,
I ended up with this layout:

```txt
     0   1   2   3   4       5   6   7   8   9   
   +---+---+---+---+---+   +---+---+---+---+---+
a  | p | y | b | k | x |   | z | f | * | * | * | 
   +---+---+---+---+---+   +---+---+---+---+---+
b  | c | i | t | r | v |   | w | a | n | s | e | 
   +---+---+---+---+---+   +---+---+---+---+---+
c  | d | u | g | h | z |   | q | m | o | l | * | 
   +---+---+---+---+---+   +---+---+---+---+---+
d              | * | * |   | * | * |
               +---+---+   +---+---+

```

#### Layout 2

Layout 1 is a good layout (significantly better than isrt and colemak in %SFBs) but I think I can do better.
Instead of having all the common action keys on the same hand, I'll put them in the middle columns like: 

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

This leaves us with 2 quad-bigrams and 6 tripple-bigrams.


#### Layout 3

Another layout I want to test will move the row-c common action keys out by 1 column.

```txt
     0   1   2   3   4       5   6   7   8   9   
   +---+---+---+---+---+   +---+---+---+---+---+
a  |   |   |   |   |   |   |   |   |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
b  |   |   |   |   |   |   |   |   |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
c  |   |   | * | * |   |   |   | * | * |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
d              | * | * |   | * | * |
               +---+---+   +---+---+

```

This layout leaves us with 2 quint-bigrams, 4 tripple-bigrams and 2 bigrams.


#### Layout 4

Once again, I wanted to see how the layout would look if I moved the row-c common action keys out by another 1 column.

```txt
     0   1   2   3   4       5   6   7   8   9   
   +---+---+---+---+---+   +---+---+---+---+---+
a  |   |   |   |   |   |   |   |   |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
b  |   |   |   |   |   |   |   |   |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
c  |   | * | * |   |   |   |   |   | * | * |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
d              | * | * |   | * | * |
               +---+---+   +---+---+

```

This layout leaves us with 2 hex-bigrams, 2 tripple-bigrams and 4 bigrams. 


#### Layout 5

The final layout I wanted to test is having two columns that only have 1 key in them. 

```txt
     0   1   2   3   4       5   6   7   8   9   
   +---+---+---+---+---+   +---+---+---+---+---+
a  |   |   | * |   |   |   |   |   | * |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
b  |   |   |   |   |   |   |   |   |   |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
c  |   |   | * |   |   |   |   |   | * |   |   | 
   +---+---+---+---+---+   +---+---+---+---+---+
d              | * | * |   | * | * |
               +---+---+   +---+---+

```