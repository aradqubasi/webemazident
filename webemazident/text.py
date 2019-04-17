from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from webemazident.db import get_db

from webemazident.utils import split_by_sentences, translate, measure

from bson.objectid import ObjectId

bp = Blueprint('text', __name__)

@bp.route('/text/new', methods=('GET', 'POST'))
def new():
    if request.method == 'GET':
        return render_template('text/new.html')
    else:
        splitted = split_by_sentences(request.form['body_text'])
        translated = [translate(sentence) for sentence in splitted]
        measured = [measure(sentence) for sentence in translated]
        text = {
            'caption' : request.form['caption'],
            'candidate' : request.form['candidate'],
            'sentences' : list([{
                'number' : i,
                'original' : splitted[i],
                'translation' : translated[i],
                'emotions' : measured[i]
            } for i in range(len(splitted))])
        }
        get_db().get_collection('texts').insert_one(text)

        return redirect(url_for('texts.index')) 
        
@bp.route('/text/edit/<id>', methods=('GET', 'POST'))
def edit(id):
    if request.method == 'GET':
        text = get_db().get_collection('texts').find_one({'_id':ObjectId(id)})
        return render_template('text/edit.html', text=text)
    elif request.method == 'POST':

        numbers = request.form.getlist('number')
        originals = request.form.getlist('original')
        translations = request.form.getlist('translation')

        surprise = request.form.getlist('surprise')
        calm = request.form.getlist('calm')
        fear = request.form.getlist('fear')
        sadness = request.form.getlist('sadness')
        anger = request.form.getlist('anger')
        disgust = request.form.getlist('disgust')

        text = {
            '_id' : ObjectId(id),
            'caption' : request.form['caption'],
            'candidate' : request.form['candidate'],
            'sentences' : list([{
                'number' : numbers[i],
                'original' : originals[i],
                'translation' : translations[i],
                'emotions' : {
                    'surprise' : surprise[i],
                    'calm' : calm[i],
                    'fear' : fear[i],
                    'sadness' : sadness[i],
                    'anger' : anger[i],
                    'disgust' : disgust[i]
                }
            } for i in range(len(numbers))])
        }
        get_db().get_collection('texts').replace_one({'_id': text['_id']}, text)
        # return render_template('text/edit.html', text=text)
        return redirect(url_for('text.edit', id=text['_id'])) 
        