import os, pandas, json
from pathlib import Path

languages = [
    "afr",
    "eng",
    "nbl",
    "nso",
    "sot",
    "ssw",
    "tsn",
    "tso",
    "ven",
    "xho",
    "zul",
]

root_path = Path(
    os.path.abspath(__file__)
).parent.parent.parent  # gov-za-sona-multilingual/

raw_data_path = Path(root_path / "data" / "raw")
proc_data_path = Path(root_path / "data" / "raw_proc")
token_data_path = Path(root_path / "data" / "tokenised")
out_path = Path(root_path / "data" / "sentence_align_output")


def build_filepath_dict():
    """
    ### Returns a dictonary of the raw data paths

    Used to locate and iterate over the data for processing
    """
    dirs = os.listdir(raw_data_path)
    dirs.remove(".gitkeep")
    dirs.sort()

    return dirs


def read_file_as_string(directory, lang):
    """
    ### Reads txt file as a string

    Used to read in a text file before passing it to the sentence tokeniser
    """
    path = Path(raw_data_path / directory / "{}.txt".format(lang))
    return open(path, "r").read()


def write_tokens_to_txt(tokens, directory, lang):
    """
    ### Writes sentence token array to a txt file

    Used after tokenisation, sentences are embedded line by line for laser.
    """
    path = Path(token_data_path / directory)
    if not os.path.exists(path):
        os.makedirs(path)

    path = Path(path / "{}.txt".format(lang))

    new = open(path, "w")
    for token in tokens:
        new.write("{}\n".format(token))

def write_txt(text, directory, lang):
    path = Path(proc_data_path / directory)
    if not os.path.exists(path):
        os.makedirs(path)

    path = Path(path / "{}.txt".format(lang))

    new = open(path, "w")
    new.write(text)


def read_file_as_array(directory_path, txt_path):  # -> str
    """
    ### Reads file as an array.

    Generally used to read tokenised data for further processing
    """
    file_path = Path(token_data_path / directory_path / "{}.txt".format(txt_path))
    return open(file_path, "r").readlines()

def write_to_jsonl(src,tgt,directory,data):
    file_name = "aligned-{}-{}.jsonl".format(src, tgt)
    file_path = out_path  / file_name

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    if file_name in os.listdir(out_path):
        f = open(file_path, 'a')
        for d in data:
            f.write(json.dumps(d) + '\n')
    else:
        f = open(file_path, 'w')
        for d in data:
            f.write(json.dumps(d) + '\n')

    print("Aligned {}-{} from  {}".format(src,tgt, directory))


def append_to_final_csv(src_lang, src_sentences, tgt_lang, tgt_sentences, sim_scores):
    """
    ### Appends to the ML aligned lang pairs .csv - creates it if it doesn't exist
    #### Params
        -   src_lang: source lang (str)
        -   src_sentences: source sentence tokens (list)
        -   tgt_lang: target lang (str)
        -   tgt_sentences: target sentence tokens (list)
        -   sim_scores: confidence scores between the pairing (list)
    """
    data = {
        "src_text": src_sentences,
        "tgt_text": tgt_sentences,
        "cosine_score": sim_scores,
    }  # build a dictonary of the info

    df = pandas.DataFrame(data)  # turn into a pandas DF

    csv_path = Path(
        "aligned_{}_{}.csv".format(src_lang, tgt_lang)
    )  # Path of lang aligned csv
    if not os.path.exists(out_path):  # if data/sentence_alignment doesnt exist
        os.makedirs(out_path)  # create it

    if os.path.exists(Path(out_path / csv_path)):  # if .csv does exist
        df.to_csv(
            Path(out_path / csv_path), mode="a", header=False, index=False
        )  # append with no headers
    else:
        df.to_csv(
            Path(out_path / csv_path), mode="w", header=True, index=False
        )  # create with headers
