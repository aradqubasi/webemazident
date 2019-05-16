import pytest
from workeremazident import utils
from unittest.mock import Mock
import urllib.request
import urllib.parse
import io
import json

def test_translate(monkeypatch):

    original = 'input text'
    # ['data']['translations'][0]['translatedText']
    translation = 'output text'
    response = {
        'data' : {
            'translations' : [
                {
                    'translatedText' : translation
                }
            ]
        }
    }

    with monkeypatch.context() as m, io.BytesIO(json.dumps(response).encode('utf-8')) as r:
        google_api_key = 'test_google_api_key'
        m.setenv('GOOGLE_API_KEY', google_api_key)

        urlopen = Mock(return_value=r)
        m.setattr(urllib.request, 'urlopen', urlopen)

        query_string = 'http://www.tempuri.org/?a=1'
        urlencode = Mock(return_value=query_string)
        m.setattr(urllib.parse, 'urlencode', urlencode)

        actual_translation = utils.google.translate(original)

        urlencode.assert_called_once()
        #pylint: disable=unpacking-non-sequence, unused-variable
        args, kwargs = urlencode.call_args
        assert len(args) == 1
        params = args[0]
        assert params['q'] == original
        assert params['source'] == 'ru'
        assert params['target'] == 'en'
        assert params['key'] == google_api_key 

        urlopen.assert_called_once()

        assert actual_translation == translation
