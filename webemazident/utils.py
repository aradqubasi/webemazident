from random import uniform
import json
import urllib.request
import urllib.parse   
from flask import current_app

def split_by_sentences(original):
    return [sentence for sentence in original.split('.') if sentence.strip() != '']

# def translate(original):
#     return ''.join([('a' if c != ' ' else ' ') for c in original])

def translate(original):
    url = "https://translation.googleapis.com/language/translate/v2" 
    params = {       
        "q": original,       
        "source": "ru",       
        "target": "en",
        "format": "text",
        "key": current_app.config['GOOGLE_API_KEY']   }      

    query_string = urllib.parse.urlencode(params)   
    data = query_string.encode("ascii")      

    with urllib.request.urlopen( url, data ) as response:        
        response_text = response.read().decode('utf-8')   
        return json.loads(
            response_text
        )['data']['translations'][0]['translatedText']
        

# def measure(sentence):
#     return {
#         'surprise': uniform(0, 10),
#         'calm': uniform(0, 10),
#         'fear': uniform(0, 10),
#         'sadness': uniform(0, 10),
#         'anger': uniform(0, 10),
#         'disgust': uniform(0, 10)
#     }

def measure(sentence):
    response = json.loads(
        urllib.request.urlopen(
            urllib.request.Request('https://qemotion.p.rapidapi.com/v1/emotional_analysis/get_emotions', headers={
                "X-RapidAPI-Key": current_app.config['RAPID_API_KEY'],
                "Content-Type": "application/json; charset=UTF-8",
                "Authorization": current_app.config['GEMOTION_AUTH_TOKEN'],
                "lang": "en",
                "text": sentence.encode("utf-8") 
            })
        ).read().decode('utf-8')
    )
    return response['content']['emotions']