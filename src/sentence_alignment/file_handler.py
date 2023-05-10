import os
from pathlib import Path

languages = ['afr', 'eng', 'nbl', 'nso', 'sot', 'ssw', 'tsn', 'tso', 'ven', 'xho', 'zul']

root_path = Path(os.path.abspath(__file__)).parent.parent.parent # gov-za-sona-multilingual/

raw_data_path = Path(root_path / 'data' / 'raw') 
token_data_path = Path(root_path / 'data' / 'tokenised') 

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