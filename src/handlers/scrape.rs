use std::io::Write;

use tokio::process::Command;



async fn flatten(repo: String) {
    
    let repo_dir = repo.replace("/", "-");

    // recursively clone the repo into data/repos/
    let output = Command::new("git")
        .arg("clone")
        .arg(format!("https://github.com/{repo}.git", repo=repo))
        .arg(format!("./data/repos/{repo_dir}", repo_dir=repo_dir))
        .arg("--recurse-submodules")
        .output();

    let output = output.await.unwrap();
    println!("status: {}", output.status);
    println!("stdout: {}", String::from_utf8_lossy(&output.stdout));
    println!("stderr: {}", String::from_utf8_lossy(&output.stderr));
    
    // for each file in the repo, recursively read it and append it to ./data/flattened/{repo_dir}.txt
    for entry in walkdir::WalkDir::new(format!("./data/repos/{repo_dir}", repo_dir=repo_dir)) {

        if entry.is_err() { continue; }

        let entry = entry.unwrap();
        let path = entry.path();

        if path.to_str().unwrap().contains(".git") { continue; }

        if path.is_file() {
            let contents = std::fs::read_to_string(path);

            if contents.is_err() { continue; }
            
            let mut file = std::fs::OpenOptions::new()
                .create(true)
                .append(true)
                .open(format!("./data/flattened/{repo_dir}.txt", repo_dir=repo_dir))
                .unwrap();

            file.write(contents.unwrap_or_default().as_bytes()).unwrap();
        }
    }

    // remove the repo directory
    let output = Command::new("rm")
        .arg("-rf")
        .arg(format!("./data/repos/{repo_dir}", repo_dir=repo_dir))
        .output();
    

}


pub async fn scrape() {

    // get list of urls from ./data/repos.txt
    let repos_raw = std::fs::read_to_string("./data/repos.txt").unwrap();

    // split the urls into a vector
    let repos: Vec<String> = repos_raw.split("\n").map(|s| s.to_string()).collect();

    // for each repo, spawn a task to clone it
    for repo in repos {
        flatten(repo).await;
    }

}