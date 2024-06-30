use std::{io::Write, path::PathBuf};
use tokio::task::JoinHandle;

use data::{Bigram, Data};

mod filter;
mod data;


async fn process(path: PathBuf) -> Data {
    let contents = std::fs::read_to_string(path).unwrap();

    let mut data = Data::default();

    for line in contents.lines() {
        for word in line.split_whitespace() {
            data.add_word(word).await;
        }
    }

    data

}



#[tokio::main]
async fn main() {

    // for each text file in data/flattened, read it, filter it and append it to data/combined.txt


    let mut target = std::fs::OpenOptions::new()
        .create(true)
        .write(true)
        .open("./data/combined.txt")
        .unwrap();

    let mut threads: Vec<JoinHandle<Data>> = Vec::new();
    let mut db = Data::default();

    for entry in walkdir::WalkDir::new("./data/flattened") {
        if entry.is_err() { continue; }
        let entry = entry.unwrap();
        let path = entry.path().to_owned(); // Clone the path
        
        if path.is_file() {
            println!("combining: {}", path.to_str().unwrap());
            let thread = tokio::spawn(process(path.to_owned())); // Pass a reference to the cloned path
            threads.push(thread);
        }
    }

    // let path = PathBuf::from("./data/flattened/0voice-interview_internal_reference.txt");
    // let thread = tokio::spawn(process(path.to_owned()));
    // threads.push(thread);

    for thread in threads {
        // wait until ALL threads are done
        let data = thread.await.unwrap();
        println!("a thread finished");
        db.merge(&data);
    }
    
    for (bigram, _) in db.bigram_count.clone().iter() {
        if !bigram.first.is_alphabetic() || !bigram.second.is_alphabetic() {
            db.bigram_count.remove(&bigram);
        }
    }

    for (trigram, _) in db.first_trigram_count.clone().iter() {
        if !trigram.first.is_alphabetic() || !trigram.second.is_alphabetic() || !trigram.third.is_alphabetic() {
            db.first_trigram_count.remove(&trigram);
        }
    }

    
    for (bigram, count) in db.bigram_count.clone().iter() {
        let reverse = Bigram { first: bigram.second, second: bigram.first };
    
        if db.bigram_count.contains_key(&reverse) && db.bigram_count.contains_key(&bigram) {        
            db.bigram_count.entry(bigram.clone()).and_modify(|e| *e += count);
            db.bigram_count.remove(&reverse);
        }
    }


    // write db to data/data.json
    let json = serde_json::to_string(&db).unwrap();
    std::fs::write("./data/data.json", json).unwrap();

}