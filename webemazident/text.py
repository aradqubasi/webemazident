from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from webemazident.db import get_db

bp = Blueprint('text', __name__)

@bp.route('/text/new', methods=('GET', 'POST'))
def new():
    if request.method == 'GET':
        return render_template('text/new.html')
    else:
        text = {
            'caption' : request.form['caption'],
            'candidate' : request.form['candidate'],
            'body_text' : request.form['body_text']
        }
        get_db().get_collection('texts').insert_one(text)
        return redirect(url_for('texts.index'))
        
        
        