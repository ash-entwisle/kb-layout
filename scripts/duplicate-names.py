
repo_names = set()


with open("../data/repos.txt", "r") as f:
    repos = f.readlines()
    
    # for each line, split at / and get the last element and check if it is in the set
    # if it is, print it, if not add it to the set
    
    for repo in repos:
        repo_name = repo.split("/")[-1]
        if repo_name in repo_names:
            print(repo_name)
        else:
            repo_names.add(repo_name)

    if len(repo_names) != len(repos):
        print("There are conflicting repo names")