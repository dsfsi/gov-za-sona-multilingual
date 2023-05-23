import file_handler, sentence_embedding, re, os
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
from pathlib import Path

root_path = Path(os.path.abspath(__file__)).parent.parent.parent # gov-za-sona-multilingual/

token_data_path = Path(root_path / 'data' / 'tokenised') 
embed_data_path = Path(root_path / 'data' / 'embed')

def cosine_score(src, tgt):        
    """
    ### Performs cosine similarity on two sentence vectors.
    #### Params 
        -   `src`: The sentence vector of the one language (list(int))
        -   `tgt`: The sentence vector of the other language (list(int))
    """
    return cosine_similarity(src.reshape(1,-1), tgt.reshape(1,-1))[0][0]

def two_lang_alignment(src_lang, tgt_lang, directory):
    """
    ### Performs sentence alignment on two languages using LASER encoded sentence vector
    #### Params 
        -   `src_lang`: The name of the one language (str)
        -   `tgt_lang`: The name of the other language (str)
        -   `edition`: The path_name of where to find the tokenised sentence .txt's (str)
    """
    src_text_path = Path(token_data_path / directory / '{}.txt'.format(src_lang))
    tgt_text_path = Path(token_data_path / directory / '{}.txt'.format(tgt_lang))
    src_embed_path = Path(embed_data_path / directory / '{}.txt'.format(src_lang))
    tgt_embed_path = Path(embed_data_path / directory / '{}.txt'.format(tgt_lang))


    src_vector = sentence_embedding.decode_sentences(directory, src_lang) # decode the src vector from the data/embed folder
    src_sentences = file_handler.read_file_as_array(directory, src_lang) # read the token sentences as array from data/tokenised folder
    tgt_sentences = file_handler.read_file_as_array(directory, tgt_lang) # read the token sentences as array from data/tokenised folder
    tgt_vector = sentence_embedding.decode_sentences(directory, tgt_lang) # decode the tgt vector from the data/embed folder
    align(src_lang, tgt_lang, src_vector, src_sentences, tgt_vector, tgt_sentences)
        
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