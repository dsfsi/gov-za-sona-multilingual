import file_handler, laser_config, sentence_tokenisation, sentence_embedding, sentence_alignment
from itertools import combinations

languages = [
    "afr",
    "eng",
    "nbl",
    "sot",
    "nso",
    "ssw",
    "tsn",
    "tso",
    "ven",
    "xho",
    "zul",
]

lang_mappings = {
    "afr": "",
    "eng": "",
    "nbl": "",
    "sot": "sot_Latn",
    "nso": "nso_Latn",
    "ssw": "ssw_Latn",
    "tsn": "tsn_Latn",
    "tso": "tso_Latn",
    "ven": "",
    "xho": "xho_Latn",
    "zul": "zul_Latn",
}


if __name__ == "__main__":
    # create directories dictionary
    filepaths_dictionary = file_handler.build_filepath_dict()
    language_pairs = list(combinations(languages, 2))

    # setup laser
    laser_config.set_environ_var()
    laser_config.setup_laser()
    laser_config.download_laser_models(lang_mappings)
    laser_config.download_tokeniser()

    # perform sentence tokenisation
    # print("Tokenising started...")
    # for directory in filepaths_dictionary:
    #     for lang in languages:
    #         text = file_handler.read_file_as_string(directory, lang)
    #         tokens = sentence_tokenisation.tokenise(text)
    #         file_handler.write_txt(sentence_tokenisation.pre_process_text(text), directory, lang)
    #         file_handler.write_tokens_to_txt(tokens, directory, lang)
    # print("Tokenising complete.")

    # # NB needs Python 3.8 due to FAISS-CPU module
    # # perform LASER encoding
    # print("LASER encoding process started...")
    # for directory in filepaths_dictionary:
    #     for lang in languages:
    #         print("Encoding {} speech for {}".format(lang, directory))
    #         sentence_embedding.encode_sentences(directory, lang, lang_mappings[lang])
    # print("LASER encoding process completed")

    # perform SA on LASER encoded sentences
    print(
        "LASER aligning process started, output will be written to .csv in the data/sentence_align_output folder."
    )
    for first_lang, sec_lang in language_pairs:
        for directory in filepaths_dictionary:
            sentence_alignment.sentence_alignment(first_lang, sec_lang, directory)
    print("LASER aligning completed")
