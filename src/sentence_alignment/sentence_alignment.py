# import file_handler, sentence_embedding, re, os
# from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
# from pathlib import Path

# filepaths_dictionary = file_handler.build_filepaths_dictonary() 

# def perform_cosine_similarity(src_vector, tgt_vector):
#     """
#     ### Performs cosine similarity on two vectors of sentence vectors
#     #### Params 
#         -   `src_vector`: The vector of sentence vectors in the one language (list(list(int))) 
#         -   `tgt_vector`: The vector of sentences vectors in the other language (list(list(int)))
#     """
#     sim_scores=[] # list to store results 
#     for i in range(len(src_vector)): # the vectors must be the same length in order to perform a valid operation
#         sim_scores.append(cosine_score(src_vector[i], tgt_vector[i])) # append the cosine score obtained from comparing sentence vectors
#     return sim_scores # return sim_scores list

# def cosine_score(src, tgt):        
#     """
#     ### Performs cosine similarity on two sentence vectors.
#     #### Params 
#         -   `src`: The sentence vector of the one language (list(int))
#         -   `tgt`: The sentence vector of the other language (list(int))
#     """
#     return cosine_similarity(src.reshape(1,-1), tgt.reshape(1,-1))[0][0]

# def two_lang_alignment(src_lang, tgt_lang, edition):
#     """
#     ### Performs sentence alignment on two languages using LASER encoded sentence vector
#     #### Params 
#         -   `src_lang`: The name of the one language (str)
#         -   `tgt_lang`: The name of the other language (str)
#         -   `edition`: The path_name of where to find the tokenised sentence .txt's (str)
#     """
#     if edition not in filepaths_dictionary[src_lang].keys(): # if the edition doesn't exist for the source lang
#         return                                               # fail
#     elif edition not in filepaths_dictionary[tgt_lang].keys(): # if the edition doesn't exist for the target lang
#         return                                                 # fail
    
#     src_txt_paths = filepaths_dictionary[src_lang][edition] # fetch the list of editions in the source lang
#     tgt_txt_paths = filepaths_dictionary[tgt_lang][edition] # fetch the list of editions in the target lang
#     src_txt_paths.sort()
#     tgt_txt_paths.sort()

#     # some explaination for the mess of code underneath
#     # an example of the variables src_txt_paths & tgt_txt_paths are:
#     # src_txts: ['2020-05-ed2-vukuzenzele-eng-01.txt', '2020-05-ed2-vukuzenzele-eng-02.txt]
#     # tgt_txts: ['2020-05-ed2-vukuzenzele-afr-02.txt', '2020-05-ed2-vukuzenzele-afr-01.txt]
#     # the problem is they are not aligned - you will get an error trying to align 'eng-01' and 'afr-02'
#     # so the messy code rectifies that
#     #
#     # I just discovered the python .sort method but I am much too tired to refactor this right now

#     for i in range(len(src_txt_paths)-1):
#         src_vector = sentence_embedding.decode_sentences(edition, src_txt_paths[i]) # decode the src vector from the data/embed folder
#         src_sentences = file_handler.read_file_as_array(edition, src_txt_paths[i]) # read the token sentences as array from data/tokenised folder
#         tgt_sentences = file_handler.read_file_as_array(edition, tgt_txt_paths[i]) # read the token sentences as array from data/tokenised folder
#         tgt_vector = sentence_embedding.decode_sentences(edition, tgt_txt_paths[i]) # decode the tgt vector from the data/embed folder
#         if len(src_vector) == len(tgt_vector) == len(src_sentences) == len(tgt_sentences): # if all the lists and vectors are the same length
#             sim_scores = perform_cosine_similarity(src_vector, tgt_vector) # obtain the list of similarity scores
#             file_handler.append_to_final_csv(src_lang,  #append all to csv
#                                             src_sentences, 
#                                             src_vector.tolist(), # turn the numpy arr into a list
#                                             tgt_lang, 
#                                             tgt_sentences, 
#                                             tgt_vector.tolist(), 
#                                             sim_scores)
        
# def simple_langs_alignment(src_lang, tgt_lang, edition):
#     """
#     ### Performs very very very basic alignment on two languages just using the tokenised .txt's
#     """
#     if edition not in filepaths_dictionary[src_lang].keys(): # if the edition doesn't exist for the source lang
#         return                                               # fail
#     elif edition not in filepaths_dictionary[tgt_lang].keys(): # if the edition doesn't exist for the target lang
#         return                                                 # fail
    
#     src_txt_paths = filepaths_dictionary[src_lang][edition] # fetch the list of editions in the source lang
#     tgt_txt_paths = filepaths_dictionary[tgt_lang][edition] # fetch the list of editions in the target lang
#     src_txt_paths.sort()
#     tgt_txt_paths.sort()

#     # similar code to 'def two_lang_alignment():'
#     for i in range(len(src_txt_paths)-1):
#         src_sentences = file_handler.read_file_as_array(edition, src_txt_paths[i]) # get the source sentences from data/tokenised
#         tgt_sentences = file_handler.read_file_as_array(edition, tgt_txt_paths[i]) # get the target sentences from data/tokenised
#         if len(src_sentences) == len(tgt_sentences): # if the list are the same length
#             file_handler.append_to_simple_csv(src_lang, src_sentences, tgt_lang, tgt_sentences) # append to simple .csv's




    
    
    
