from random import uniform

def split_by_sentences(original):
    return original.split('.')

def translate(original):
    return ''.join([('a' if c != ' ' else ' ') for c in original])

def measure(sentence):
    return {
        'surprise': uniform(0, 10),
        'calm': uniform(0, 10),
        'fear': uniform(0, 10),
        'sadness': uniform(0, 10),
        'anger': uniform(0, 10),
        'disgust': uniform(0, 10)
    }