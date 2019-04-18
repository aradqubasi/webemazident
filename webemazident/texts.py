from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from webemazident.db import get_db

from bson.objectid import ObjectId

bp = Blueprint('texts', __name__, url_prefix='/texts')

@bp.route('/index', methods=('GET',))
def index():
    if request.method == 'GET':
        texts = get_db().get_collection('texts').find({})
        return render_template('texts/index.html', texts=texts)
