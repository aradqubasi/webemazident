import pytest
from bson import ObjectId

@pytest.fixture
def sample_gemotion_text():
    return {
        # '_id' : object_id,
        'caption': 'Thief',
        'author': 'The People',
        'language': 'en',
        'raw_text_head': {
            'text_id' : ObjectId(),
            'caption': 'Thief',
            'author': 'The People',
            'language': 'ru'
        },
        'sentiment': {
            'happiness' : 0.14285714285714285,
            'surprise' : 0.14285714285714285,
            'calm' : 0.14285714285714285,
            'fear' : 0.14285714285714285,
            'sadness' : 0.14285714285714285,
            'anger' : 0.14285714285714285,
            'disgust' : 0.14285714285714285
        },
        # 'processed_by_job': object_id,
        'sentences': [
            {
                'order_number' : 0,
                'original' : 'Карл у карлы украл корралы',
                'translated' : 'Karl stole corrals from Carla',
                'sentiment' : {
                    'happiness' : 1.0,
                    'surprise' : 1.0,
                    'calm' : 1.0,
                    'fear' : 1.0,
                    'sadness' : 1.0,
                    'anger' : 1.0,
                    'disgust' : 1.0
                }
            }, {
                'order_number' : 1,
                'original' : 'Карла у Карла украла кларнет',
                'translated' : 'Carla Karl stole the clarinet',
                'sentiment' : {
                    'happiness' : 22.0,
                    'surprise' : 22.0,
                    'calm' : 22.0,
                    'fear' : 22.0,
                    'sadness' : 22.0,
                    'anger' : 22.0,
                    'disgust' : 22.0
                }
            }
        ]
    }