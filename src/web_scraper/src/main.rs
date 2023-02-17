mod helpers;
mod trans_struct;

use helpers::{
    build_data_filepath, compile_links, compile_string, compile_trans_links, create_file,
    get_webpage, write_to_file, TransLinksCompilationErrs,
};

use trans_struct::TransStruct;

fn main() {
    let base_page = get_webpage("https://www.gov.za/state-nation-address").unwrap();
    let base_links = compile_links(&base_page);

    let mut trans_vec: Vec<TransStruct> = Vec::new();
    for link in base_links {
        let sona_page = get_webpage(link.as_str()).unwrap();
        let trans_struct = compile_trans_links(sona_page.as_str());
        if let Ok(trans) = trans_struct {
            trans_vec.push(trans);
        } else if let Err(err) = trans_struct {
            match err {
                TransLinksCompilationErrs::LongerThan11(title) => {
                    println!("Identified list is longer than 11 elements for {}", title)
                }
                TransLinksCompilationErrs::MissingTranslationBlock(title) => {
                    println!("Missing translation block for {}", title)
                }
                TransLinksCompilationErrs::MissingDate(title) => {
                    println!("No date present on {}", title)
                }
                TransLinksCompilationErrs::MissingTranslationList(title) => {
                    println!("No translations available for {}", title)
                }
            }
        }
    }

    for trans in trans_vec {
        let file_path = build_data_filepath(trans.get_date());

        create_file(file_path.clone());

        for lang in trans.keys() {
            if let Ok(page) = get_webpage(trans.get_link(lang).unwrap().as_str()) {
                let text = compile_string(&page);
                write_to_file(text, file_path.clone(), lang.to_owned());
            }
        }
    }
}
