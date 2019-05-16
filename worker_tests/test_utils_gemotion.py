import pytest
import urllib.request
import io
from unittest.mock import Mock, MagicMock
from workeremazident import utils
import json

def test_rank(monkeypatch):
    sentiment = {
        'happiness' : 1, 
        'surprise' : 1, 
        'calm' : 1, 
        'fear' : 1, 
        'sadness' : 1, 
        'anger' : 1, 
        'disgust' : 1
    }
    response = {
        'content' : {
            'emotions' : sentiment
        }
    }
    with monkeypatch.context() as m, io.BytesIO(json.dumps(response).encode('utf-8')) as r:
        #prepare
        rapid_api_key = 'test_rapid_api_key'
        m.setenv('RAPID_API_KEY', rapid_api_key)

        gemotion_auth_token = 'test_gemotion_auth_token'
        m.setenv('GEMOTION_AUTH_TOKEN', gemotion_auth_token)

        urlopen = Mock(return_value=r)
        m.setattr(urllib.request, 'urlopen', urlopen)

        concrete_request = MagicMock()
        Request = Mock(return_value=concrete_request)
        m.setattr(urllib.request, 'Request', Request)

        #test
        actual_sentiment = utils.gemotion.rank('Abc')

        #assert
        assert actual_sentiment == sentiment

        urlopen.assert_called_once_with(concrete_request)

        Request.assert_called_once()

        #pylint: disable=unpacking-non-sequence, unused-variable
        args, kwargs = Request.call_args
        assert rapid_api_key == kwargs['headers']['X-RapidAPI-Key']
        assert gemotion_auth_token == kwargs['headers']['Authorization']

def test_calculate_average_sentiment(sample_gemotion_text):
    
    avg_sentiment = utils.gemotion.calculate_average_sentiment(sample_gemotion_text)

    assert avg_sentiment == sample_gemotion_text['sentiment']

def test_get_emotion_symbols():

    emotions = utils.gemotion.get_emotion_symbols()

    assert ['happiness', 'surprise', 'calm', 'fear', 'sadness', 'anger', 'disgust'] == emotions