import nltk, re, os

# import file_handler


def fix_end_of_sentence(text: str):  # -> str
    """
    ### Adds a space after the end of a sentence without a space
    #### Example
    The tokeniser will interpret this as a whole sentence.A human reader can detect the missing space.

    It also doesn't make .co.za & co.za split up because that would be lame.
    """
    end_of_sentece_chars = [".", "?", "!", ";"]  # Chars a sentence could end with
    i = 0  # index
    while (
        i < len(text) - 1
    ):  # while i less the length minus 1 because we refer to i+1 in the body
        if text[i] in end_of_sentece_chars:  # if text[char] is the end of a sentence
            if (
                ord(text[i + 1]) >= 97 and ord(text[i + 1]) <= 122
            ):  # check if char in front of sentence bewtween a-z
                text = " ".join(
                    [text[: i + 1], text[i + 1 :]]
                )  # add a space between the sentence and following char
        i += 1  # Onto the next char

    return text


def pre_process_text(text):  # -> str
    text = text.lower()
    text = re.sub("\s{2,}", " ", text)
    text = re.sub("\;", ".", text)
    text = re.sub("\[", "", text)
    text = re.sub("\]", ".", text)
    text = fix_end_of_sentence(text)
    
    return text


def tokenise(text):  # -> str
    text = pre_process_text(text)  # clean data
    # print(text)
    return nltk.tokenize.sent_tokenize(text)  # tokenise data
