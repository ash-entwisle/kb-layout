use std::{collections::HashMap, hash::Hash};

use serde::{Deserialize, Serialize};
use tokio::sync::RwLock;
use once_cell::sync::Lazy;

use crate::filter::filter;

pub static mut DATA: Lazy<RwLock<Data>> = Lazy::new(|| {
    RwLock::new(Data {
        bigram_count: HashMap::new(),
        first_trigram_count: HashMap::new(),
        char_alpha_count: HashMap::new(),
        char_other_count: HashMap::new(),
    })
});

#[derive(Eq, PartialEq, Hash, Clone, Copy, Debug, Deserialize)]
pub struct Bigram {
    pub first: char,
    pub second: char,
}

impl std::fmt::Display for Bigram {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}{}", self.first, self.second)
    }
}

impl Serialize for Bigram {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::ser::Serializer,
    {
        format!("{}", self).serialize(serializer)
    }
}


#[derive(Eq, PartialEq, Hash, Clone, Copy, Debug, Deserialize)]
pub struct Trigram {
    pub first: char,
    pub second: char,
    pub third: char,
}

impl std::fmt::Display for Trigram {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}{}{}", self.first, self.second, self.third)
    }
}

impl Serialize for Trigram {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::ser::Serializer,
    {
        format!("{}", self).serialize(serializer)
    }
}


#[derive(Eq, PartialEq, Clone, Debug, Serialize, Deserialize)]
pub struct Data {

    pub bigram_count: HashMap<Bigram, u128>,
    pub first_trigram_count: HashMap<Trigram, u128>,
    pub char_alpha_count: HashMap<char, u128>,
    pub char_other_count: HashMap<char, u128>,

}

impl Data {
    pub async fn add_word(&mut self, word: &str) {
        let mut chars = word.chars();
        let mut first = filter(chars.next().unwrap_or_default()).await;
        let mut second = filter(chars.next().unwrap_or_default()).await;
        let mut third = filter(chars.next().unwrap_or_default()).await;

        if first.is_alphabetic() {
            self.char_alpha_count.entry(first).and_modify(|e| *e += 1).or_insert(1);
        } else {
            self.char_other_count.entry(first).and_modify(|e| *e += 1).or_insert(1);
        }

        if second.is_alphabetic() {
            self.char_alpha_count.entry(second).and_modify(|e| *e += 1).or_insert(1);
        } else {
            self.char_other_count.entry(second).and_modify(|e| *e += 1).or_insert(1);
        }

        if third.is_alphabetic() {
            self.char_alpha_count.entry(third).and_modify(|e| *e += 1).or_insert(1);
        } else {
            self.char_other_count.entry(third).and_modify(|e| *e += 1).or_insert(1);
        }

        self.first_trigram_count.entry(Trigram { first, second, third }).and_modify(|e| *e += 1).or_insert(1);

        for c in chars {
            let c = filter(c).await;

            if c.is_alphabetic() {
                self.char_alpha_count.entry(c).and_modify(|e| *e += 1).or_insert(1);
            } else {
                self.char_other_count.entry(c).and_modify(|e| *e += 1).or_insert(1);
            }

            self.bigram_count.entry(Bigram { first, second }).and_modify(|e| *e += 1).or_insert(1);
            
            first = second;
            second = third;
            third = c;
        }
    }

    pub fn merge(&mut self, other: &Data) {
        for (k, v) in other.bigram_count.iter() {
            self.bigram_count.entry(*k).and_modify(|e| *e += v).or_insert(*v);
        }

        for (k, v) in other.first_trigram_count.iter() {
            self.first_trigram_count.entry(*k).and_modify(|e| *e += v).or_insert(*v);
        }

        for (k, v) in other.char_alpha_count.iter() {
            self.char_alpha_count.entry(*k).and_modify(|e| *e += v).or_insert(*v);
        }

        for (k, v) in other.char_other_count.iter() {
            self.char_other_count.entry(*k).and_modify(|e| *e += v).or_insert(*v);
        }
    }
}

impl Default for Data {
    fn default() -> Self {
        Data {
            bigram_count: HashMap::new(),
            first_trigram_count: HashMap::new(),
            char_alpha_count: HashMap::new(),
            char_other_count: HashMap::new(),
        }
    }
}

