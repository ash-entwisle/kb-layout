use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

struct Data {
    best_score: f64,
    min_cap: f64,
    best_g1: String,
    best_g2: String,
    best_g3: String,
    best_g4: String,
    best_g5: String,
    best_g6: String,
    
}

async fn handle_part(
    best_score: f64, min_cap: f64,
    g1: String, g1_score: f64,
    home_row_chars: Vec<char>, 
    n3_bigram_score: HashMap<String, f64>, 
    n6_bigram_score: HashMap<String, f64>
) -> Option<Data> {

    let mut data = Data {
        best_score: best_score,
        min_cap: min_cap,
        best_g1: g1.clone(),
        best_g2: String::new(),
        best_g3: String::new(),
        best_g4: String::new(),
        best_g5: String::new(),
        best_g6: String::new(),
    };

    if g1_score > data.min_cap 
    || g1_score > data.best_score 
    || !g1.chars().any(|c| home_row_chars.contains(&c)
    ) {
        return None;
    }

    for (g2, &g2_score) in &n3_bigram_score {

        if g1_score > data.best_score {
            break;
        }

        if g1_score > data.best_score 
        || g2_score > data.min_cap 
        || g2_score > data.best_score 
        || g2.chars().any(|c| g1.clone().contains(c)) 
            || !g2.chars().any(|c| home_row_chars.contains(&c)
        ) {
            continue;
        }

        for (g3, &g3_score) in &n3_bigram_score {

            if g1_score + g2_score > data.best_score {
                break;
            }

            if g1_score + g2_score > data.best_score 
            || g3_score > data.min_cap 
            || g3_score > data.best_score 
            || g3.chars().any(|c| g1.contains(c) 
                || g2.contains(c)
            ) {
                continue;
            }

            for (g4, &g4_score) in &n3_bigram_score {
                
                if g1_score + g2_score + g3_score > data.best_score {
                    break;
                }

                if g1_score + g2_score + g3_score > data.best_score 
                || g4_score > data.min_cap 
                || g4_score > data.best_score 
                || g4.chars().any(|c| g1.contains(c) 
                    || g2.contains(c) 
                    || g3.contains(c)
                ) {
                    continue;
                }

                for (g5, &g5_score) in &n6_bigram_score {

                    if g1_score + g2_score + g3_score + g4_score > data.best_score {
                        break;
                    }

                    if g1_score + g2_score + g3_score + g4_score > data.best_score 
                    || g5_score > data.min_cap 
                    || g5_score > data.best_score 
                    || g5.chars().any(|c| g1.contains(c) 
                        || g2.contains(c) 
                        || g3.contains(c) 
                        || g4.contains(c)
                    ) {
                        continue;
                    }

                    for (g6, &g6_score) in &n6_bigram_score {

                        if g1_score + g2_score + g3_score + g4_score + g5_score > data.best_score {
                            break;
                        }

                        let total_score = g1_score + g2_score + g3_score + g4_score + g5_score + g6_score;
                        if total_score > data.best_score 
                        || g6_score > data.min_cap 
                        || g6_score > data.best_score 
                        || g6.chars().any(|c| g1.contains(c) 
                            || g2.contains(c) 
                            || g3.contains(c)  
                            || g4.contains(c) 
                            || g5.contains(c)
                        ) {
                            continue;
                        }

                        if total_score < best_score {
                            data.best_score = total_score;
                            data.best_g1 = g1.clone();
                            data.best_g2 = g2.clone();
                            data.best_g3 = g3.clone();
                            data.best_g4 = g4.clone();
                            data.best_g5 = g5.clone();
                            data.best_g6 = g6.clone();
                        }
                    }
                }
            }
        }
    }

    Some(data)
}

pub async fn layout_5(){
    let home_row_chars: Vec<char> = "etaisrno".chars().collect();
    let best_score = 2 as f64;
    let min_cap = 0.75;

    // let n3_bigram_score = read_csv("../data/n-bigram/n3_bigram_score.csv")?;
    // let n6_bigram_score = read_csv("../data/n-bigram/n6_bigram_score.csv")?;

    let n3_bigram_score: HashMap<String, f64> = include_str!("../../data/n-bigram/n3_bigram_score.csv")
        .lines()
        .skip(1)
        .map(|line| {
            let parts: Vec<&str> = line.split(',').collect();
            let key = parts[0].to_string();
            let value: f64 = parts[1].parse().unwrap();
            (key, value)
        })
        .into_iter()
        .filter(|(_, v)| v < &&min_cap)
        .map(|(k, v)| (k.clone(), v))
        .collect();
    
    let n6_bigram_score: HashMap<String, f64> = include_str!("../../data/n-bigram/n6_bigram_score.csv")
        .lines()
        .skip(1)
        .map(|line| {
            let parts: Vec<&str> = line.split(',').collect();
            let key = parts[0].to_string();
            let value: f64 = parts[1].parse().unwrap();
            (key, value)
        })
        .into_iter()
        .filter(|(_, v)| v < &&min_cap)
        .map(|(k, v)| (k.clone(), v))
        .collect();

    // print n3 and n6 bigram scores
    
    println!("n3_bigram_score: {:?}", n3_bigram_score);

    // let mut n3_bigram_score = HashMap::new();

    // for line in n3_bigram_raw.lines().skip(1) {
    //     let parts: Vec<&str> = line.split(',').collect();
    //     let key = parts[0].to_string();
    //     let value: f64 = parts[1].parse().unwrap();
    //     n3_bigram_score.insert(key, value);
    // }

    // n3_bigram_raw = n3_bigram_score.into_iter()
    //     .filter(|(_, v)| v > &&min_cap)
    //     .map(|(k, v)| (k.clone(), v))
    //     .collect();

    // let mut n6_bigram_score = HashMap::new();

    // for line in n6_bigram_raw.lines().skip(1) {
    //     let parts: Vec<&str> = line.split(',').collect();
    //     let key = parts[0].to_string();
    //     let value: f64 = parts[1].parse().unwrap();
    //     n6_bigram_score.insert(key, value);
    // }

    // n6_bigram_score = n6_bigram_score.into_iter()
    //     .filter(|(_, v)| v > &&min_cap)
    //     .map(|(k, v)| (k.clone(), v))
    //     .collect();

    let mut data = Data {
        best_score: best_score,
        min_cap: min_cap,
        best_g1: String::new(),
        best_g2: String::new(),
        best_g3: String::new(),
        best_g4: String::new(),
        best_g5: String::new(),
        best_g6: String::new(),
    };

    let mut threads = Vec::new();

    for (g1, &g1_score) in &n3_bigram_score {
        threads.push(tokio::spawn(handle_part(
            data.best_score, data.min_cap,
            g1.clone(), g1_score,
            home_row_chars.clone(),
            n3_bigram_score.clone(),
            n6_bigram_score.clone()
        )));

        println!("spawned thread...")
    }

    // // just do one for now
    // let (g1, &g1_score) = n6_bigram_score.iter().next().unwrap();
    // threads.push(tokio::spawn(handle_part(
    //     data.best_score, data.min_cap,
    //     g1.clone(), g1_score,
    //     home_row_chars.clone(),
    //     n3_bigram_score.clone(),
    //     n6_bigram_score.clone()
    // )));

    println!("All threads spawned...");


    for thread in threads {
        let result = thread.await.unwrap();
        if let Some(result) = result {
            if result.best_score < data.best_score {
                data.best_score = result.best_score;
                data.best_g1 = result.best_g1;
                data.best_g2 = result.best_g2;
                data.best_g3 = result.best_g3;
                data.best_g4 = result.best_g4;
                data.best_g5 = result.best_g5;
                data.best_g6 = result.best_g6;
            }
        }
        println!("thread finished...");
        println!("Best Score: {}", data.best_score);
    }

    println!("Best Score: {}", data.best_score);
    println!("{} {} {} {} {} {}", data.best_g1, data.best_g2, data.best_g3, data.best_g4, data.best_g5, data.best_g6);
}
