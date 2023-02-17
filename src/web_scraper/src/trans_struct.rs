use std::{collections::{HashMap, hash_map::Keys}};
use lazy_static::lazy_static;

#[derive(Debug)]
pub struct TransStruct {
    date: String,
    trans_links: HashMap<String, String>
}



lazy_static! {
    static ref MONTH_MAP: HashMap<&'static str, &'static str> = {
        let mut map = HashMap::new();
        map.insert("Jan", "01");
        map.insert("Feb", "02");
        map.insert("Mar", "03");
        map.insert("Apr", "04");
        map.insert("May", "05");
        map.insert("Jun", "06");
        map.insert("Jul", "07");
        map.insert("Aug", "08");
        map.insert("Sep", "09");
        map.insert("Oct", "10");
        map.insert("Nov", "11");
        map.insert("Dec", "12");
        map
    };
}

impl TransStruct {
    pub fn new(date: String) -> Self {
        let parts = date.split(' ').collect::<Vec<&str>>();
        let f_date = format!("{}-{}-{}", parts[2], MONTH_MAP[parts[1]], parts[0]);

        Self{date: f_date, trans_links: HashMap::new()}
    }

    pub fn get_link(&self, key: &String) -> Option<&String> {
        self.trans_links.get(key)
    }
    
    pub fn get_date(&self) -> String {
        self.date.clone()
    }

    pub fn insert(&mut self, key: String, val: String) -> Option<String> {
        self.trans_links.insert(key, val)
    }

    pub fn keys(&self) -> Keys<'_, String, String>{
        self.trans_links.keys()
    }
}