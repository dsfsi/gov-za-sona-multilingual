# import file_handler, sentence_embedding, re, os
# from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
# from pathlib import Path

# root_path = Path(
#     os.path.abspath(__file__)
# ).parent.parent.parent  # gov-za-sona-multilingual/

# token_data_path = Path(root_path / "data" / "tokenised")
# embed_data_path = Path(root_path / "data" / "embed")


# def cosine_score(src, tgt):
#     """
#     ### Performs cosine similarity on two sentence vectors.
#     #### Params
#         -   `src`: The sentence vector of the one language (list(int))
#         -   `tgt`: The sentence vector of the other language (list(int))
#     """
#     return cosine_similarity(src.reshape(1, -1), tgt.reshape(1, -1))[0][0]


# def two_lang_alignment(src_lang, tgt_lang, directory):
#     """
#     ### Performs sentence alignment on two languages using LASER encoded sentence vector
#     #### Params
#         -   `src_lang`: The name of the one language (str)
#         -   `tgt_lang`: The name of the other language (str)
#         -   `directory`: The path_name of where to find the tokenised sentence .txt's (str)
#     """
#     src_text_path = Path(token_data_path / directory / "{}.txt".format(src_lang))
#     tgt_text_path = Path(token_data_path / directory / "{}.txt".format(tgt_lang))
#     src_embed_path = Path(embed_data_path / directory / "{}.txt".format(src_lang))
#     tgt_embed_path = Path(embed_data_path / directory / "{}.txt".format(tgt_lang))

#     src_vector = sentence_embedding.decode_sentences(
#         directory, src_lang
#     )  # decode the src vector from the data/embed folder
#     src_sentences = file_handler.read_file_as_array(
#         directory, src_lang
#     )  # read the token sentences as array from data/tokenised folder
#     tgt_sentences = file_handler.read_file_as_array(
#         directory, tgt_lang
#     )  # read the token sentences as array from data/tokenised folder
#     tgt_vector = sentence_embedding.decode_sentences(
#         directory, tgt_lang
#     )  # decode the tgt vector from the data/embed folder
#     align(src_lang, tgt_lang, src_vector, src_sentences, tgt_vector, tgt_sentences)


# def align(src_lang, tgt_lang, src_vector, src_sentences, tgt_vector, tgt_sentences):
#     used_sentences = []
#     loop_iter = min(
#         len(src_vector), len(src_sentences), len(tgt_sentences), len(tgt_vector)
#     )

#     src = []
#     tgt = []
#     cos = []
#     for i in range(loop_iter):
#         similarity_dict = {}
#         for j in range(loop_iter - 1):
#             if j in used_sentences:
#                 continue
#             else:
#                 src_sent = src_vector[i]
#                 tgt_sent = tgt_vector[i]
#                 sim_score = cosine_score(src_sent, tgt_sent)
#                 similarity_dict[j] = sim_score

#         max_similar = max(similarity_dict, key=similarity_dict.get, default=0)
#         used_sentences.append(max_similar)

#         src.append(src_sentences[i])
#         tgt.append(tgt_sentences[max_similar])
#         cos.append(sim_score)

#     file_handler.append_to_final_csv(src_lang, src, tgt_lang, tgt, cos)

import file_handler, sentence_embedding
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
from pprint import pprint
filepaths_dictionary = file_handler.build_filepaths_dictonary() 


def cosine_score(src, tgt):        
    """
    ### Performs cosine similarity on two sentence vectors.
    #### Params 
        -   `src`: The sentence vector of the one language (list(int))
        -   `tgt`: The sentence vector of the other language (list(int))
    """
    return cosine_similarity(src.reshape(1,-1), tgt.reshape(1,-1))[0][0]

def align(src,tgt,vectors, tokens):
  (i,j) = (0,0)
  src_vect, tgt_vect = vectors
  src_tokens, tgt_tokens = tokens
  sentences = []
  while i < len(src_vect) and j < len(tgt_vect):
    score = cosine_score(src_vect[i], tgt_vect[j])
    if i==0 and score < 0.7:
      return None
    elif score < 0.6: 
      return sentences
    else:
      sentence = {
        src : src_tokens[i],
        tgt : tgt_tokens[j],
        "score" : str(score),
      }
      # print(sentence)
      sentences.append(sentence)
    (i,j) = (i+1, j+1)
  return sentences
  
def update_indices(indexes, vectors):
    (i, j) = indexes
    (best_i, best_j) = (-1, -1)
    src_vect, tgt_vect = vectors
    threshold = 0.7

    for x in range(0, 3):
        for y in range(0, 3):
            i_temp, j_temp = i + y, j + x

            if i_temp < len(src_vect) and j_temp < len(tgt_vect):
                score = cosine_score(src_vect[i_temp], tgt_vect[j_temp])
                
                if score > threshold:
                    (best_i, best_j) = (i_temp, j_temp)
                    break

        if best_i != -1 and best_j != -1:
            break

    if best_i != -1 and best_j != -1: 
      return (best_i, best_j)
    else: return (i+1, j+1)
  
  
def sentence_alignment(src, tgt, directory):
  if directory not in filepaths_dictionary[src].keys(): # if the directory doesn't exist for the source lang
      return                                               # fail
  elif directory not in filepaths_dictionary[tgt].keys(): # if the directory doesn't exist for the target lang
      return                                                 # fail
  
  src_txt_paths = filepaths_dictionary[src][directory] # fetch the list of directorys in the source lang
  tgt_txt_paths = filepaths_dictionary[tgt][directory] # fetch the list of directorys in the target lang
  src_txt_paths.sort()
  tgt_txt_paths.sort()
  
  shortest = min(len(src_txt_paths), len(tgt_txt_paths))

  for i in range(shortest): 
    src_tokens = file_handler.read_file_as_array(directory, src_txt_paths[i])
    tgt_tokens = file_handler.read_file_as_array(directory, tgt_txt_paths[i])
    src_vectors = sentence_embedding.decode_sentences(directory, src_txt_paths[i])
    tgt_vectors = sentence_embedding.decode_sentences(directory, tgt_txt_paths[i])
    aligned_sentences = []
    (i,j) = (0,0)
    factor = 5
    while i+factor < len(src_tokens) and j+factor < len(tgt_tokens):
      # print(f"src: {i+factor} - {len(src_tokens)}")
      # print(f"tgt: {j+factor} - {len(tgt_tokens)}")
      some_sentences = align(src, tgt, (src_vectors[i:i+factor], tgt_vectors[j:j+factor]), (src_tokens[i:i+factor], tgt_tokens[j:j+factor]))
      if some_sentences != None and len(some_sentences) > 0:
        aligned_sentences.extend(some_sentences)
        length = len(some_sentences)
        (i,j) = (i+length, j+length)
      else:
        (last_i,last_j) = (i,j)
        (i,j) = update_indices((i,j), (src_vectors, tgt_vectors))
        if (last_i,last_j) == (i,j):
          print("failed to realign indexes, exiting...")
          break
      
    file_handler.write_to_jsonl(src, tgt, directory, aligned_sentences)

    