import json
import urllib.request
import urllib.parse  
import os

def rank(sentence):
    rapid_api_key = os.environ.get('RAPID_API_KEY')
    gemotion_auth_token = os.environ.get('GEMOTION_AUTH_TOKEN')
    response = json.loads(
        urllib.request.urlopen(
            urllib.request.Request('https://qemotion.p.rapidapi.com/v1/emotional_analysis/get_emotions', headers={
                "X-RapidAPI-Key": rapid_api_key,
                "Content-Type": "application/json; charset=UTF-8",
                "Authorization": gemotion_auth_token,
                "lang": "en",
                "text": sentence.encode("utf-8") 
            })
        ).read().decode('utf-8')
    )
    return response['content']['emotions']

def get_emotion_symbols():
    return ['happiness', 'surprise', 'calm', 'fear', 'sadness', 'anger', 'disgust']

def calculate_average_sentiment(gemotion_text):
    emotions = get_emotion_symbols()
    ttl_sentiment = 0
    ttl_sentiment_per_emotion = {emotion : 0 for emotion in get_emotion_symbols()}
    for sentence in gemotion_text['sentences']:
        for emotion in emotions:
            ttl_sentiment_per_emotion[emotion] += sentence['sentiment'][emotion]
    ttl_sentiment = sum([value for emotion, value in ttl_sentiment_per_emotion.items()])
    for emotion in emotions:
        ttl_sentiment_per_emotion[emotion] /= ttl_sentiment
    return ttl_sentiment_per_emotion