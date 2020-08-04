import functools
import json
from utils import uog
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

@courses_bp.route('/', methods={'POST'})
def getCourses():
    courses = uog.webadvisorQuery(request.form or json.loads(request.data))
    only_data = courses['data'].values();
    return render_template('results.html', title='Results', courses=only_data), 200 if courses['success'] else 400