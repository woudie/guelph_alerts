import functools
import json
from utils import uog
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)



bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/', methods={'GET'})
def home():
    return render_template('home.html', subjects=config['subjects'], test="Henlo")