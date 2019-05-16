from bson import ObjectId
import pymongo
import os
from workeremazident import utils

INITIALIZING = 'initializing'
ERROR = 'error'
DONE = 'done'

def execute(task):
    task_id = ObjectId()
    db = pymongo.MongoClient(os.environ.get('CONNECTION_STRING')).get_database(os.environ.get('DATABASE'))
    db.get_collection('job_receipts').insert_one({
        '_id' : task_id,
        'status' : INITIALIZING
    })
    try:
        if task.type == 'split_then_google_translate_then_gemotion_sentiment':
            text_id = task.text_id
            text = db.get_collection('texts').find_one({'_id' : text_id})
            db.get_collection('job_receipts').update_one({
                '_id' : task_id
            }, {
                '$set' : {
                    'text_id' : text_id
                }
            })

            subjob_order_number = 0

            #splitting
            split_subjob = {
                'subjob_id' : ObjectId(),
                'type' : 'utils.text.split_by_sentences',
                'status' : INITIALIZING,
                'order_number' : subjob_order_number
            }
            splitted = []
            try:
                splitted = utils.text.split_by_sentences(text['text'])
                split_subjob['status'] = DONE
                split_subjob['result'] = splitted
            except Exception as ex:
                split_subjob['status'] = ERROR
                split_subjob['exception'] = ex.__str__()
            db.get_collection('job_receipts').update_one({
                    '_id' : task_id
                }, {
                    '$push' : {
                        'subjob_receipts' : split_subjob
                    }
                })
            subjob_order_number += 1

            #translating
            translate_subjob = {
                'subjob_id' : ObjectId(),
                'type' : 'utils.google.translate',
                'status' : INITIALIZING,
                'order_number' : subjob_order_number
            }
            translated = []
            last_sentence = ''
            try:
                source = text['language']
                EN = 'en'
                sentence_order_number = 0
                for sentence in splitted:
                    last_sentence = sentence
                    translated.append({
                        'order_number' : sentence_order_number,
                        'original' : sentence,
                        'translated' : utils.google.translate(sentence, source=source, target=EN)
                    })
                    sentence_order_number += 1
                translate_subjob['status'] = DONE
                translate_subjob['result'] = translated
            except Exception as ex:
                translate_subjob['status'] = ERROR
                translate_subjob['exception'] = ex.__str__()
                translate_subjob['result'] = translated
                translate_subjob['last_sentence'] = last_sentence
            db.get_collection('job_receipts').update_one({
                '_id' : task_id
            }, {
                '$push' : {
                    'subjob_receipts' : translate_subjob
                }
            })
            subjob_order_number += 1
            
            #ranking
            rank_subjob = {
                'subjob_id' : ObjectId(),
                'type' : 'utils.gemotion.rank',
                'status' : INITIALIZING,
                'order_number' : subjob_order_number
            }
            ranked = []
            last_ranked = ''
            try:
                for sentence in translated:
                    last_ranked = sentence['translated']
                    ranked.append({
                        'order_number' : sentence['order_number'],
                        'original' : sentence['original'],
                        'translated' : last_ranked,
                        'sentiment' : utils.gemotion.rank(last_ranked)
                    })
                rank_subjob['status'] = DONE
            except Exception as ex:
                rank_subjob['status'] = ERROR
                rank_subjob['exception'] = ex.__str__()
                rank_subjob['last_ranked'] = last_ranked
            rank_subjob['result'] = ranked
            db.get_collection('job_receipts').update_one({
                '_id' : task_id
            }, {
                '$push' : {
                    'subjob_receipts' : rank_subjob
                }
            })

            #creating gemotion_text
            gemotion_text = {
                'caption' : text['caption'],
                'author' : text['author'],
                'language' : EN,
                'raw_text_head' : {
                    'text_id' : text_id,
                    'caption' : text['caption'],
                    'author' : text['author'],
                    'language' : text['language']
                },
                'processed_by_job' : task_id,
                'sentences' : ranked
            }
            gemotion_text['sentiment'] = utils.gemotion.calculate_average_sentiment(gemotion_text)
            db.get_collection('gemotion_texts').insert_one(gemotion_text)
            db.get_collection('job_receipts').update_one({
                '_id' : task_id
            }, {
                '$set' : {
                    'status' : DONE
                }
            })
    except Exception as ex:
        print(ex)
        db.get_collection('job_receipts').update_one({
            '_id' : task_id
        }, {
            '$set' : {
                'exception' : ex.__str__(),
                'status' : ERROR
            }
        })
    

