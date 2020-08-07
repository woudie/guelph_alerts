import functools
from flask import (current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, json)

from apscheduler.schedulers.background import BackgroundScheduler

from utils.db import (emails, courses)
from utils.communication import Communication
from utils.worker import course_polling

comm = Communication()

sched = BackgroundScheduler(daemon=True)
sched.start()

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/', methods={'GET'})
def cart():
    return render_template('cart.html', title="Cart")

@bp.route('/submit', methods={'POST'})
def submit():
    res = json.loads(request.data)
    
    theEmail = emails.objects(email__in=[res['email']])
    if len(theEmail) != 0:
        return {"success":"true", "message":"Email is already registered"}
    
    comm.initEmail(res['email'])
    
    theEmail = emails(email=res['email'])
    theEmail.save()
    
    for course in res['courses']:
        theCourse = courses.objects(course__in=[ course['Section Name and Title'] ])
        if len(theCourse) == 0:
            sched.add_job(course_polling, 'interval', seconds=10, args=[ course['Section Name and Title'], sched ], id=course['Section Name and Title'])
            
        theCourse = theCourse[0] if len(theCourse) > 0 else courses(course=course['Section Name and Title'], all_emails=[])
        theCourse.save()
        theCourse.all_emails.append(theEmail)
        theCourse.save()
        
    return {"success": "true", "message":""}