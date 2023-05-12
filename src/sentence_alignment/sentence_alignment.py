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