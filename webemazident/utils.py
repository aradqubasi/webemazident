from random import uniform
import json
import urllib.request
import urllib.parse   

def split_by_sentences(original):
    return original.split('.')

# def translate(original):
#     return ''.join([('a' if c != ' ' else ' ') for c in original])

def translate(original):
    url = "https://translation.googleapis.com/language/translate/v2" 
    params = {       
        "q": [ "Не кто странствуют потерялись", ],       
        "source": "ru",       
        "target": "en",
        "format": "text",
        "key": "AIzaSyBdYpwqAQI9nPP-VAdAF-51oz8-H_XYOnw"   }      

    query_string = urllib.parse.urlencode(params)   
    data = query_string.encode("ascii")      

    with urllib.request.urlopen( url, data ) as response:        
        response_text = response.read().decode('utf-8')     
        return json.loads(
            json.loads(
                response_text
            )['data']['translations'][0]['translatedText']
        )[0]

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
                "X-RapidAPI-Key": "4b77b0bfc8msha1e193906f5df01p149009jsn4171810ad2fd",
                "Content-Type": "application/json; charset=UTF-8",
                "Authorization": "Token token=\"bc55ca0a8f5c8c41556f499a93f7077a\"",
                "lang": "en",
                "text": sentence  
            })
        ).read().decode('utf-8')
    )
    return response['content']['emotions']