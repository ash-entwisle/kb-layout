
with open("../data/repos.txt", "r") as f:
    repos = f.readlines()
    
    for i in range(len(repos)):
        repo = repos[i]
        repo = repo.strip()
        repo = repo.split("/")
        repo = "/".join(repo[-2:])
        repos[i] = repo
    
    with open("../data/repos.txt", "w") as f:
        for repo in repos:
            f.write(repo + "\n")