from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from webemazident.db import get_db

bp = Blueprint('texts', __name__, url_prefix='/texts')

@bp.route('/index', methods=('GET',))
def index():
    texts = [
        {
            'candidate': 'Ze',
            'caption': 'Ze Interview',
            'sentences': [
                {
                    'number': 1,
                    'original': 'Кравчук говорит мудрые вещи',
                    'translation': 'Kravchuk says wise things',
                    'emotions': {
                        'happiness': 0,
                        'surprise': 0,
                        'calm': 0,
                        'fear': 0,
                        'sadness': 0,
                        'anger': 0,
                        'disgust': 0
                    }
                }, {
                    'number': 2,
                    'original': 'Вот последнее, что я слышал по телевизору, он говорил о военном полож...',
                    'translation': 'Here is the last thing I heard on TV, he talked about the martial law',
                    'emotions': {
                        'happiness': 0,
                        'surprise': 0,
                        'calm': 1,
                        'fear': 9,
                        'sadness': 9,
                        'anger': 0,
                        'disgust': 0
                    }
                }, {
                    'number': 3,
                    'original': 'Звучит это достаточно мудро',
                    'translation': 'It sounds wise enough',
                    'emotions': {
                        'happiness': 0,
                        'surprise': 0,
                        'calm': 2,
                        'fear': 9,
                        'sadness': 9,
                        'anger': 0,
                        'disgust': 5
                    }
                }
            ]
        },
        {
            'candidate': 'Ze',
            'caption': '13 Thesises',
            'sentences': [
                {
                    'number': 1,
                    'original': ' Сложно охарактеризовать его, как президента, быть первым всегда сложно',
                    'translation': 'Difficult to characterize him as president, to be first is always difficult',
                    'emotions': {
                        'happiness': 0,
                        'surprise': 15,
                        'calm': 2,
                        'fear': 14,
                        'sadness': 29,
                        'anger': 0,
                        'disgust': 5
                    }
                }, {
                    'number': 2,
                    'original': ' Но, я думаю, он хотел что-то сделать хорошее для нашей страны',
                    'translation': 'But, I think he wanted to do something good for our country.',
                    'emotions': {
                        'happiness': 0,
                        'surprise': 15,
                        'calm': 8,
                        'fear': 14,
                        'sadness': 32,
                        'anger': 0,
                        'disgust': 5
                    }
                }, {
                    'number': 3,
                    'original': 'А Леонид Данилович - простой рубаха-парень',
                    'translation': 'And Leonid Danilovich - a simple shirt-guy',
                    'emotions': {
                        'happiness': 0,
                        'surprise': 15,
                        'calm': 8,
                        'fear': 14,
                        'sadness': 41,
                        'anger': 0,
                        'disgust': 5
                    }
                }
            ]
        }
    ]

    return render_template('texts/index.html', texts=texts)