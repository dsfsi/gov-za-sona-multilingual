import file_handler, sentence_embedding, re, os
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
from pathlib import Path

filepaths_dictionary = file_handler.build_filepaths_dictonary() 


def cosine_score(src, tgt):        
    """
    ### Performs cosine similarity on two sentence vectors.
    #### Params 
        -   `src`: The sentence vector of the one language (list(int))
        -   `tgt`: The sentence vector of the other language (list(int))
    """
    return cosine_similarity(src.reshape(1,-1), tgt.reshape(1,-1))[0][0]

def two_lang_alignment(src_lang, tgt_lang, edition):
    """
    ### Performs sentence alignment on two languages using LASER encoded sentence vector
    #### Params 
        -   `src_lang`: The name of the one language (str)
        -   `tgt_lang`: The name of the other language (str)
        -   `edition`: The path_name of where to find the tokenised sentence .txt's (str)
    """
    if edition not in filepaths_dictionary[src_lang].keys(): # if the edition doesn't exist for the source lang
        return                                               # fail
    elif edition not in filepaths_dictionary[tgt_lang].keys(): # if the edition doesn't exist for the target lang
        return                                                 # fail
    
    src_txt_paths = filepaths_dictionary[src_lang][edition] # fetch the list of editions in the source lang
    tgt_txt_paths = filepaths_dictionary[tgt_lang][edition] # fetch the list of editions in the target lang
    src_txt_paths.sort()
    tgt_txt_paths.sort()

    # some explaination for the mess of code underneath
    # an example of the variables src_txt_paths & tgt_txt_paths are:
    # src_txts: ['2020-05-ed2-vukuzenzele-eng-01.txt', '2020-05-ed2-vukuzenzele-eng-02.txt]
    # tgt_txts: ['2020-05-ed2-vukuzenzele-afr-02.txt', '2020-05-ed2-vukuzenzele-afr-01.txt]
    # the problem is they are not aligned - you will get an error trying to align 'eng-01' and 'afr-02'
    # so the messy code rectifies that
    #
    # I just discovered the python .sort method but I am much too tired to refactor this right now

    
    

    for i in range(len(src_txt_paths)-1):
        src_vector = sentence_embedding.decode_sentences(edition, src_txt_paths[i]) # decode the src vector from the data/embed folder
        src_sentences = file_handler.read_file_as_array(edition, src_txt_paths[i]) # read the token sentences as array from data/tokenised folder
        tgt_sentences = file_handler.read_file_as_array(edition, tgt_txt_paths[i]) # read the token sentences as array from data/tokenised folder
        tgt_vector = sentence_embedding.decode_sentences(edition, tgt_txt_paths[i]) # decode the tgt vector from the data/embed folder
        align(src_lang, tgt_lang, src_vector, src_sentences, tgt_vector, tgt_sentences)
        # if len(src_vector) == len(tgt_vector) == len(src_sentences) == len(tgt_sentences): # if all the lists and vectors are the same length
            # sim_scores = perform_cosine_similarity(src_vector, tgt_vector) # obtain the list of similarity scores
            # file_handler.append_to_final_csv( #append all to csv
        #                                     src_sentences,          
        #                                     tgt_sentences, 
        #                                     sim_scores)
        
def align(src_lang, tgt_lang, src_vector, src_sentences, tgt_vector, tgt_sentences): 
    used_sentences = []
    loop_iter = min(len(src_vector), len(src_sentences), len(tgt_sentences), len(tgt_vector))

    src = []
    tgt = []
    cos = []
    for i in range(loop_iter): 
        similarity_dict = {}
        for j in range(loop_iter-1):
            if j in used_sentences:
                continue
            else:
                src_sent = src_vector[i]
                tgt_sent = tgt_vector[i]
                sim_score = cosine_score(src_sent,tgt_sent)
                similarity_dict[j] = sim_score

        max_similar = max(similarity_dict, key = similarity_dict.get,default=0)
        used_sentences.append(max_similar)

        src.append(src_sentences[i])
        tgt.append(tgt_sentences[max_similar])
        cos.append(sim_score)

    file_handler.append_to_final_csv(src_lang, src, tgt_lang, tgt, cos)