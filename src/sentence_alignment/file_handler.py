import os, pandas
from pathlib import Path

languages = ['afr', 'eng', 'nbl', 'nso', 'sot', 'ssw', 'tsn', 'tso', 'ven', 'xho', 'zul']

root_path = Path(os.path.abspath(__file__)).parent.parent.parent # gov-za-sona-multilingual/

raw_data_path = Path(root_path / 'data' / 'raw') 
token_data_path = Path(root_path / 'data' / 'tokenised') 
output_data_path = Path(root_path / 'data' / 'sentence_align_output')

def build_filepath_dict():
    dirs = os.listdir(raw_data_path)
    dirs.remove('.gitkeep')
    dirs.sort()

    return dirs

    
def read_file_as_string(edition, lang):
    path = Path(raw_data_path / edition / '{}.txt'.format(lang))
    return open(path, 'r').read()

def write_tokens_to_txt(tokens, edition, lang):
    path = Path(token_data_path / edition)
    if not os.path.exists(path):
        os.makedirs(path)

    path = Path(path / '{}.txt'.format(lang))

    new = open(path, 'w')
    for token in tokens:
        new.write('{}\n'.format(token))

def read_file_as_array(edition_path, txt_path): # -> str
    """
    ### Reads file as an array.

    Generally used to read tokenised data for further processing
    """
    file_path = Path(token_data_path / edition_path / '{}.txt'.format(txt_path))
    return open(file_path, 'r').readlines() 

def append_to_final_csv(src_lang, src_sentences, tgt_lang, tgt_sentences , sim_scores):
    """
    ### Appends to the ML aligned lang pairs .csv - creates it if it doesn't exist
    #### Params
        -   src_lang: source lang (str)
        -   src_sentences: source sentence tokens (list)
        -   src_vector: source sentence vectors (list)
        -   tgt_lang: target lang (str)
        -   tgt_sentences: target sentence tokens (list)
        -   tgt_vector: target sentence vectors (list)
        -   sim_scores: confidence scores between the pairing (list)
    """
    data = {
        'src_text' : src_sentences,
        'tgt_text' : tgt_sentences,
        'cosine_score' : sim_scores
    } # build a dictonary of the info

    df = pandas.DataFrame(data) #turn into a pandas DF

    csv_path = Path('aligned_{}_{}.csv'.format(src_lang, tgt_lang)) # Path of lang aligned csv
    if not os.path.exists(output_data_path): # if data/sentence_alignment doesnt exist
        os.makedirs(output_data_path) # create it 

    if os.path.exists(Path(output_data_path / csv_path)): # if .csv does exist
        df.to_csv(Path(output_data_path / csv_path), mode='a',header=False, index=False) # append with no headers
    else: 
        df.to_csv(Path(output_data_path / csv_path), mode='w',header=True, index=False) # create with headers

