import json
import urllib.request
import urllib.parse  
import os

def translate(original, source='ru', target='en'):
    google_api_key = os.environ.get('GOOGLE_API_KEY')
    url = "https://translation.googleapis.com/language/translate/v2" 
    params = {       
        "q": original,       
        "source": source,       
        "target": target,
        "format": "text",
        "key": google_api_key   }      

    query_string = urllib.parse.urlencode(params)   
    data = query_string.encode("ascii")      

    with urllib.request.urlopen( url, data ) as response:        
        response_text = response.read().decode('utf-8')   
        return json.loads(
            response_text
        )['data']['translations'][0]['translatedText']