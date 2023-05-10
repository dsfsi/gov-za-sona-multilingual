# import laser_config, file_handler, sentence_tokenisation, sentence_embedding, sentence_alignment
import file_handler, laser_config, sentence_tokenisation, sentence_embedding
from itertools import combinations

languages = ['afr', 'eng', 'nbl', 'sot', 'nso', 'ssw', 'tsn', 'tso', 'ven', 'xho', 'zul']

lang_mappings = {
                    'afr' : '',
                    'eng' : '',
                    'nbl' : '',
                    'sot' : 'sot_Latn',
                    'nso' : 'nso_Latn',
                    'ssw' : 'ssw_Latn',
                    'tsn' : 'tsn_Latn',
                    'tso' : 'tso_Latn',
                    'ven' : '',
                    'xho' : 'xho_Latn',
                    'zul' : 'zul_Latn',
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
    print("Tokenising started...")
    for directory in filepaths_dictionary:
        for lang in languages:
            text = file_handler.read_file_as_string(directory, lang)
            tokens = sentence_tokenisation.tokenise(text)
            file_handler.write_tokens_to_txt(tokens, directory, lang)
    print("Tokenising complete.")


    # perform LASER encoding
    print("LASER encoding process started...")
    for directory in filepaths_dictionary:
        for lang in languages:  
            print("Encoding {} speech for {}".format(lang, directory))
            sentence_embedding.encode_sentences(directory, lang, lang_mappings[lang])
    print("LASER encoding process completed")



    #     # perform SA on LASER encoded sentences
    #     print("LASER aligning process started, output will be written to .csv in the data/sentence_align_output folder.")
    #     for (first_lang, sec_lang) in language_pairs:
    #         for edition in edition_keys:
    #             sentence_alignment.two_lang_alignment(first_lang, sec_lang, edition)
    #     print("LASER aligning completed")



    #     # perform basic sentece alignment on tokenised sentences
    #     print("Simple aligning process started, output will be written to .csv in the data/simple_align_output folder.")
    #     for (first_lang, sec_lang) in language_pairs:
    #         for edition in edition_keys:
    #             sentence_alignment.simple_langs_alignment(first_lang, sec_lang, edition)
    #     print("Simple aligning completed")
        
    #     # write last edition reviewed to file so as not to review in future
    #     file_handler.write_latest_edition(edition_keys[len(edition_keys)-1])
    # else: print('No new editions present to perform sentence alignment')

