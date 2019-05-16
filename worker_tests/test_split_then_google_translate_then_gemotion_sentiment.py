import pytest
from unittest.mock import Mock, call
import os
import mongomock
import pymongo
from bson import ObjectId
import workeremazident
from collections import namedtuple

Task = namedtuple('Task', ['task_id', 'type', 'text_id'])

mongo_connection_string = 'mongodb://tempuri.org:27017'
mongo_database = 'test'

@mongomock.patch(servers=(mongo_connection_string,))
def test_execute(monkeypatch, sample_gemotion_text):

    with monkeypatch.context() as m:
        # mongo_connection_string = 'mongodb://tempuri.org:27017'
        # mongo_database = 'test'
        environment_variables = {
            'CONNECTION_STRING' : mongo_connection_string,
            'DATABASE' : mongo_database
        }
        os_environ_get = Mock(side_effect=lambda key: environment_variables[key])
        m.setattr(os.environ, 'get', os_environ_get)
        
        # m.setattr(pymongo, 'MongoClient', mongomock.MongoClient)
        text_id = sample_gemotion_text['raw_text_head']['text_id']
        db = pymongo.MongoClient(mongo_connection_string)\
            .get_database(mongo_database)
        raw_text = {
            '_id' : text_id,
            'caption': 'Thief',
            'author': 'The People',
            'language': 'ru',
            'text' : '.'.join(sentence['original'] for sentence in sample_gemotion_text['sentences'])
        }
        db.get_collection('texts').insert_one(raw_text)

        split_by_sentences = Mock(side_effect=lambda text: [s['original'] for s in sample_gemotion_text['sentences']])
        m.setattr(workeremazident.utils.text, 'split_by_sentences', split_by_sentences)

        translate = Mock(side_effect=lambda sentence, source, target: [s['translated'] for s in sample_gemotion_text['sentences'] if s['original'] == sentence][0])
        m.setattr(workeremazident.utils.google, 'translate', translate)

        rank = Mock(side_effect=lambda sentence: [s['sentiment'] for s in sample_gemotion_text['sentences'] if s['translated'] == sentence][0])
        m.setattr(workeremazident.utils.gemotion, 'rank', rank)

        task = Task(ObjectId(), 'split_then_google_translate_then_gemotion_sentiment', text_id)

        #------------

        workeremazident.tasks.execute(task)
        
        #------------

        split_by_sentences.assert_called_once_with(raw_text['text'])

        translate.assert_has_calls([
            call(sample_gemotion_text['sentences'][0]['original'], source='ru', target='en'),
            call(sample_gemotion_text['sentences'][1]['original'], source='ru', target='en')
        ])
        assert translate.call_count == 2

        rank.assert_has_calls([
            call(sample_gemotion_text['sentences'][0]['translated']),
            call(sample_gemotion_text['sentences'][1]['translated'])
        ])
        assert rank.call_count == 2

        actual_job_receipt = pymongo.MongoClient(mongo_connection_string).get_database(mongo_database).get_collection('job_receipts').find_one()
        assert actual_job_receipt is not None
        assert actual_job_receipt['status'] == 'done'
        
        actual_gemotion_texts = list(pymongo.MongoClient(mongo_connection_string).get_database(mongo_database).get_collection('gemotion_texts').find())
        assert len(actual_gemotion_texts) == 1
        
        actual_gemotion_text = actual_gemotion_texts[0]
        assert type(actual_gemotion_text.pop('_id')) is ObjectId
        assert type(actual_gemotion_text.pop('processed_by_job')) is ObjectId
        assert sample_gemotion_text == actual_gemotion_text
        
        