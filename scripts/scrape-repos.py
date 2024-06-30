import requests
import re

# MD files to scrape
md_files = [
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/C.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/CPP.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/CSS.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/CSharp.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Clojure.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/CoffeeScript.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/DM.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Dart.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Elixir.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Go.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Groovy.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/HTML.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Haskell.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Java.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/JavaScript.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Julia.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Kotlin.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Lua.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/MATLAB.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Objective-C.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/PHP.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Perl.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/PowerShell.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Python.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/R.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Ruby.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Rust.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Scala.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Shell.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Swift.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/TeX.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Top-100-forks.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Top-100-stars.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/TypeScript.md",
    "https://raw.githubusercontent.com/EvanLi/Github-Ranking/master/Top100/Vim-script.md",
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