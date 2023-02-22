extern crate reqwest;

use std::{fs::{self}, collections::HashMap, io::Write, env, path::PathBuf};

use reqwest::{Error};
use scraper::{Html, Selector};

use lazy_static::lazy_static;

use crate::trans_struct::TransStruct;

// lang_mappings = {
//     'afr' : '',
//     'eng' : '',
//     'nbl' : '',
//     'nso' : 'sot_Latn',
//     'sep' : 'nso_Latn',
//     'ssw' : 'ssw_Latn',
//     'tsn' : 'tsn_Latn',
//     'tso' : 'tso_Latn',
//     'ven' : '',
//     'xho' : 'xho_Latn',
//     'zul' : 'zul_Latn',
// } 

lazy_static! {
    static ref MAIN_DIV: Selector = Selector::parse(".field-items").unwrap();
    static ref TEXT_DIV: Selector = Selector::parse(".field-type-text-with-summary").unwrap();
    static ref PARA: Selector = Selector::parse("p").unwrap();
    static ref TRANS_BLOCK: Selector = Selector::parse(".language-switcher-locale-url").unwrap();
    static ref TITLE: Selector = Selector::parse("#page-title").unwrap();
    static ref DATE: Selector = Selector::parse(".date-display-single").unwrap();
    static ref HEAD2: Selector = Selector::parse("h2").unwrap();
    static ref LIST: Selector = Selector::parse("ul").unwrap();
    static ref LIST_ELEMENT: Selector = Selector::parse("li").unwrap();

    static ref LANG_MAP: HashMap<&'static str, &'static str> = {
        let mut map = HashMap::new();
        map.insert("English", "eng");
        map.insert("Afrikaans", "afr");
        map.insert("isiNdebele", "nbl");
        map.insert("isiXhosa", "xho");
        map.insert("isiZulu", "zul");
        map.insert("Sesotho", "sot");
        map.insert("Sesotho sa Leboa", "nso");
        map.insert("Setswana", "tsn");
        map.insert("Siswati", "ssw"); 
        map.insert("siSwati", "ssw"); // THIS IS NOT A DUPLICATE
        map.insert("Tshivenda", "ven");
        map.insert("Xitsonga", "tso");
        map
    };

    static ref ABBR_MAP: HashMap<&'static str, &'static str> = {
        let mut map = HashMap::new();
        map.insert("en", "eng");
        map.insert("af", "afr");
        map.insert("nr", "nbl");
        map.insert("xh", "xho");
        map.insert("zu", "zul");
        map.insert("st", "sot");
        map.insert("nso", "nso");
        map.insert("tn", "tsn");
        map.insert("ss", "ssw");
        map.insert("ve", "ven");
        map.insert("ts", "tso");
        map
    };
}

const BASE_PATH: &str = "https://www.gov.za";

pub fn get_webpage(url: &str) -> Result<String, Error> {
    let response = reqwest::blocking::get(url)?;
    response.text()
}

pub fn compile_links(page: &str) -> Vec<String> {

    let document = Html::parse_document(page);
    let mut main_div = document.select(&MAIN_DIV);
    let fragment = main_div.next().unwrap();
    let full_lists = fragment.select(&LIST);

    let mut formatted_lists: Vec<String> = full_lists
        .into_iter()
        .filter(|list| {
            if let Some(ele) = list.parent() {
                ele.value().as_element().unwrap().name() != "li"
            } else {
                false
            }
        })
        .filter(|list| {
            if list.first_child().unwrap().first_child().is_some() {
                if let Some(elememt) = list
                    .first_child()
                    .unwrap()
                    .first_child()
                    .unwrap()
                    .value()
                    .as_element()
                {
                    elememt.name() != "strong"
                } else {
                    false
                }
            } else {
                false
            }
        })
        .map(|list| {
            let child = list.first_child().unwrap().first_child().unwrap();
            if child.value().as_element().unwrap().name() == "span" {
                child.first_child().unwrap()
            } else {
                child
            }
        })
        .map(|element| element.value().as_element().unwrap().attr("href").unwrap())
        .map(|element| {
            let http_selection = &element[0..5];
            if !http_selection.cmp("https").is_eq() {
                format!("{}{}", BASE_PATH, element)
            } else {
                element.to_string()
            }
        }).collect();

    formatted_lists.pop();
    formatted_lists
}


pub enum TransLinksCompilationErrs {
    LongerThan11(String),
    MissingTranslationBlock(String),
    MissingDate(String),
    MissingTranslationList(String),
    DateAfterMostRecent(String)
}

pub fn compile_trans_links(page: &str) -> Result<TransStruct, TransLinksCompilationErrs> {
    let document = Html::parse_document(page);    
    let trans_count = document.select(&TRANS_BLOCK).count(); //kill me
    let last_date = read_latest_date();
    let title = document.select(&TITLE).next().unwrap().first_child().unwrap().value().as_text().unwrap().to_string();
    if trans_count != 0 {
        
        let date = document.select(&DATE).next().unwrap().first_child().unwrap().value().as_text().unwrap().to_string();
        let mut trans_struct = TransStruct::new(date);
        if last_date >= trans_struct.get_date() {
            return Err(TransLinksCompilationErrs::DateAfterMostRecent(title));
        }

        let trans_block = document.select(&TRANS_BLOCK).next().unwrap();
        let block_children = trans_block.children();
        
        for child in block_children {
            let lang_tag_full = child.value().as_element().unwrap().attr("class").unwrap();
            let lang_tag_trim = lang_tag_full.split(' ').collect::<Vec<&str>>()[0].to_string();
            let proper_lang_abbr = ABBR_MAP[lang_tag_trim.as_str()].to_string();
            let pre_link = child.first_child().unwrap().value().as_element().unwrap().attr("href").unwrap();
            let post_link = format!("{}{}", BASE_PATH, pre_link);
            trans_struct.insert(proper_lang_abbr, post_link);
        }
        println!("Found translation links for {}", title);
        Ok(trans_struct)
    } else if trans_count == 0 {
        if let Some(date) = document.select(&DATE).next() {
            let date_str = date.first_child().unwrap().value().as_text().unwrap().to_string();
            let mut trans_struct = TransStruct::new(date_str);
            if last_date > trans_struct.get_date() {
                return Err(TransLinksCompilationErrs::DateAfterMostRecent(title));
            }
            let fragment = document.select(&TEXT_DIV).next().unwrap();
            if let Some(trans_list) = fragment.select(&LIST).next() {
                let links = trans_list.children();
                if links.clone().count() == 11 {
                    for link in links {
                        let pre_link =  link.first_child().unwrap().value().as_element().unwrap().attr("href").unwrap();
                        let key = link.first_child().unwrap().first_child().unwrap().value().as_text().unwrap().to_string();
                        let lang_tag = LANG_MAP[&key.as_str()].to_string();
                        let post_link = format!("{}{}", BASE_PATH, pre_link);
                        trans_struct.insert(lang_tag, post_link);
                    }
                    println!("Found translation links for {}", title);
                    Ok(trans_struct)
                } else {
                    Err(TransLinksCompilationErrs::LongerThan11(title))
                }
            } else {
                Err(TransLinksCompilationErrs::MissingTranslationBlock(title))
            }
        } else {
            Err(TransLinksCompilationErrs::MissingDate(title))
        }
    } else {
        Err(TransLinksCompilationErrs::MissingTranslationList(title))
    }
} 

pub fn compile_string(page: &str) -> String {
    let document = Html::parse_document(page);
    let fragment = document.select(&TEXT_DIV).next().unwrap();
    let paragraphs = fragment.select(&PARA);

    let mut compiled_string = String::from("");
    for p in paragraphs {
        let text = p.text().collect::<Vec<_>>().join("");
        compiled_string = compiled_string + text.as_str();
    }

    compiled_string
}

pub fn build_data_filepath(date: String) -> String {

    
    let script_path = env::current_exe().unwrap();
    let parent_path = script_path.parent().unwrap().parent().unwrap().parent().unwrap();
    let relative_path = format!("data/raw/SONA_{}", date);
    let mut path = PathBuf::new();
    path.push(parent_path);
    path.push(relative_path);

    path.to_str().unwrap().into()
}

pub fn create_file(file_path: String) {
    match fs::create_dir(file_path.clone()) {
        Ok(()) => {}
        Err(error) => println!("Error creating {}: {}", file_path, error),
    }
}

pub fn write_to_file(text: String, file_path: String, file_name: String) {

    let file_name = format!("{}/{}.txt", file_path, file_name);

    match fs::File::create(file_name.clone()) {
        Ok(mut file) => match file.write_all(text.as_bytes()) {
            Ok(()) => {},
            Err(error) => println!("Error writing to file: {}", error),
        },
        Err(error) => println!("Error creating file: {}", error),
    }
}

pub fn read_latest_date() -> String {

    let script_path = env::current_exe().unwrap();
    let parent_path = script_path.parent().unwrap().parent().unwrap().parent().unwrap();
    let relative_path = "data/raw/";
    let mut path = PathBuf::new();

    path.push(parent_path);
    path.push(relative_path);
    
    let entries = fs::read_dir(path).unwrap();

    let mut file_names: Vec<String> = entries
        .map(|entry| entry.unwrap().file_name().into_string().unwrap())
        .collect();

    file_names.sort_by(|a, b| b.cmp(a));

    let name = file_names.first().unwrap();
    if name == ".gitkeep" {
        return "0000-00-00".into()
    }
    let date = &name[5..];
    date.into()
}