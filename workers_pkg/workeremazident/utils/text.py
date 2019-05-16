def split_by_sentences(original):
    return [sentence for sentence in original.split('.') if sentence.strip() != '']