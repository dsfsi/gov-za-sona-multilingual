import os, json
import file_handler, sentence_embedding
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
from pprint import pprint
filepaths_dictionary = file_handler.build_filepath_dict() 

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
  # if directory not in filepaths_dictionary[src].keys(): # if the directory doesn't exist for the source lang
  #     return                                               # fail
  # elif directory not in filepaths_dictionary[tgt].keys(): # if the directory doesn't exist for the target lang
  #     return                                                 # fail
  root_path = Path(
    os.path.abspath(__file__)
  ).parent.parent.parent  # gov-za-sona-multilingual/

  
  src_tokens = file_handler.read_file_as_array(directory, src)
  tgt_tokens = file_handler.read_file_as_array(directory, tgt)
  src_vectors = sentence_embedding.decode_sentences(directory, src)
  tgt_vectors = sentence_embedding.decode_sentences(directory, tgt)

  aligned_sentences = []
  (i,j) = (0,0)
  factor = 5
  while i+factor < len(src_tokens) and j+factor < len(tgt_tokens):
    # print(f"{src}: {i+factor} - {len(src_tokens)}")
    # print(f"{tgt}: {j+factor} - {len(tgt_tokens)}")
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

  