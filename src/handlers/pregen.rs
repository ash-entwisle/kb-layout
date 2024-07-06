use std::collections::{HashMap, HashSet};

use std::io::{BufRead, Write};
use std::vec::IntoIter;
use std::{fs::File, io::BufReader};

use itertools::Itertools;
use tokio::task::JoinHandle;


async fn check_handler(
    perms: Vec<&&String>, 
    filter_score: &'static f64,
    nbg_score: &'static HashMap<String, f64>,
) -> Option<(Vec<String>, f64)> {
    
    let mut score = 0.0;
    let mut name: Vec<String> = Vec::new();
    let mut letters: Vec<char> = Vec::new();


    // TODO: move this to join handle
    // let mut perm_perms = perms.clone();

    // // get all permutations of perms, check if any are present in perms_score
    // for perm in perm_perms.iter().permutations(perms.len()) {
    //     let perm = perm.iter().map(|s| s.to_string()).collect::<Vec<String>>();
    //     let perm = perm.join("-");

    //     if perms_score.contains_key(&perm) {
    //         return None;
    //     }
    // }

    // for bigram in &perms {
    //     for c in bigram.chars() {
    //         if letters.contains(&c) { return None; }
    //         letters.push(c);
    //     }
    // }

    for bigram in perms {
        score += nbg_score.get(*bigram).unwrap();
        if &score > filter_score { return None; }
        name.push(bigram.to_string());
    }

    Some((name, score))
}


pub async fn pregen() {

    let nbg_to_calc: u8 = 2;
    let perms_to_calc: u8 = 2;
    static FILTER_SCORE: f64 = 1.6;

    let nbg_file = format!("./data/n-bigram/n{}_bigram_score_filtered.csv", nbg_to_calc);
    let out_file = format!("./data/pregen/{}n{}_bigram_score_filtered.csv", perms_to_calc, nbg_to_calc);

    // open n-bigram file
    let file = File::open(nbg_file).unwrap();
    let reader = BufReader::new(file);

    println!("reading data...");

    // skip header, for each, add to hashmap
    let mut nbg_score: HashMap<String, f64> = HashMap::new();

    println!("parsing data...");

    let mut lines: u32 = 0;

    for line in reader.lines().skip(1) {
        let line = line.unwrap();
        let mut parts = line.split(',');
        let bigram = parts.next().unwrap().to_string();
        let score = parts.next().unwrap().parse::<f64>().unwrap();
        nbg_score.insert(bigram, score);

        lines += 1;
    }

    let nbg_score: &'static HashMap<String, f64> = Box::leak(Box::new(nbg_score));

    let keys = nbg_score.keys().collect::<Vec<&String>>();
    let keys: &'static Vec<&String> = Box::leak(Box::new(keys));

    // for each n permutation, calculate score
    let mut perms_score: HashMap<String, f64> = HashMap::new();
    let mut perms_calculating: HashSet<String> = HashSet::new();

    let perms = keys.iter().permutations(perms_to_calc as usize).unique();

    let mut threads: Vec<JoinHandle<Option<(Vec<String>, f64)>>> = Vec::new();
    let len: usize = (lines as f64).powi(perms_to_calc as i32) as usize;

    println!("calculating {} permutations...", len);

    for perm in perms {

        let mut letters: Vec<char> = Vec::new();
        let mut to_break = false;

        for bigram in &perm {
            for c in bigram.chars() {
                if letters.contains(&c) { 
                    to_break = true;
                    break;
                }
                letters.push(c);
            }
        }

        let name_perms = perm.clone();

        for perm_perm in name_perms.iter().permutations(perms_to_calc as usize) {
            let perm_perm = perm_perm.iter().map(|s| s.to_string()).collect::<Vec<String>>();
            let perm_perm = perm_perm.join("-");

            if perms_calculating.contains(&perm_perm) {
                to_break = true;
                break;
            } else {
                perms_calculating.insert(perm_perm);
            }
        }

        if to_break { 
            continue; 
        }

        let task: JoinHandle<Option<(Vec<String>, f64)>> = tokio::spawn(
            async move {
                check_handler(perm, &FILTER_SCORE, nbg_score).await
            }
        );

        threads.push(task);
    }

    let thread_count = threads.len();
    println!("waiting for {} threads...", thread_count);

    for thread in threads {

        let result = thread.await.unwrap();

        if result.is_none() { continue; }

        let (name, score) = result.unwrap();

        // for perm in name_perms.iter().permutations(perms_to_calc as usize) {
        //     let perm = perm.iter().map(|s| s.to_string()).collect::<Vec<String>>();
        //     let perm = perm.join("-");

        //     if perms_score.contains_key(&perm) {
        //         continue;
        //     }
        // }

        let name = name.join("-");
   
        perms_score.insert(name, score);

    }

    println!("sorting and writing to file...");

    // sort by score, ascending
    let perms_score: IntoIter<(String, f64)> = perms_score.into_iter()
        .sorted_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap());

    // open outfile to write
    let mut writer = File::create(out_file).unwrap();

    // write header
    writer.write_all(b"bigram,score\n").unwrap();

    for (bigram, score) in perms_score {
        writer.write_all(format!("{},{}\n", bigram, score).as_bytes()).unwrap();
    }



}