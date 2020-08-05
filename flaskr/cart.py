import functools
import json
from utils.communication import Communication
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)

comm = Communication()

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/', methods={'GET'})
def cart():
    return render_template('cart.html', title="Cart")

@bp.route('/submit', methods={'POST'})
def submit():
    res = json.loads(request.data)
    comm.initEmail(res['email']);
    return {"success": "true"}