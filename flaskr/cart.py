import functools
import json
from utils.communication import Communication
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from utils.db import (emails, courses)

comm = Communication()

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/', methods={'GET'})
def cart():
    return render_template('cart.html', title="Cart")

@bp.route('/submit', methods={'POST'})
def submit():
    res = json.loads(request.data)
    comm.initEmail(res['email'])
    
    theEmail = emails.objects(email__in=[res['email']])
    if len(theEmail) != 0:
        return {"success":"true", "message":"Email is already registered"}
    
    theEmail = emails(email=res['email']).save()
    
    for course in res['courses']:
        theCourse = courses.objects(course__in=[ course['Section Name and Title'] ])
        if len(theCourse) == 0:
            theCourse = courses(course=course['Section Name and Title'])
            theCourse.save()
        theCourse.all_emails.append(theEmail)
        theCourse.save()
    return {"success": "true", "message":""}