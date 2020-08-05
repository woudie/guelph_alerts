import functools
import json
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

bp = Blueprint('home', __name__, url_prefix='/')

with open('flaskr/utils/uog_config.json') as f:
    config = json.load(f)

@bp.route('/', methods={'GET'})
def home():
    return render_template('home.html', title="Home", subjects=config['subjects'])

@bp.route('/faq', methods={'GET'})
def faq():
    return render_template('faq.html', title="FAQ")