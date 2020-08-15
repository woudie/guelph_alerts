import os
import functools
from flask import (current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, json)
from datetime import (datetime, timedelta)

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore

from utils.db import (emails, courses)
from utils.communication import Communication
from utils.worker import course_polling
from utils.helper import cleanup_email

comm = Communication()
db_uri = "mongodb+srv://{user}:{passw}@cluster0-czbyg.mongodb.net/GuelphAlerts?retryWrites=true&w=majority"
    
jobstores = {
  'default': MongoDBJobStore(database='apscheduler', 
                             collection='jobs', 
                             host=db_uri.format(user=os.environ['DB_USERNAME'], passw=os.environ['DB_PASSWORD']),
                             port=27017)
}

sched = BackgroundScheduler(daemon=True, jobstores=jobstores)
sched.start()
sched.add_job(cleanup_email, trigger='cron', hour='4', minute='20')

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/', methods={'GET'})
def cart():
    return render_template('cart.html', title="Cart")

@bp.route('/submit', methods={'POST'})
def submit():
    res = json.loads(request.data)
    end_date = ( datetime.utcnow() + timedelta(days=14) ) 
    
    theEmail = emails.objects(email__in=[res['email']])
    if len(theEmail) != 0:
        return {"success":"true", "message":"Email is already registered"}
    
    comm.initEmail(res['email'])
    
    theEmail = emails(email=res['email'], expire=end_date.strftime('%Y-%m-%d'))
    theEmail.save()
    
    for course in res['courses']:
        theCourse = courses.objects(course__in=[ course['Section Name and Title'] ])
        
        theCourse = theCourse[0] if len(theCourse) > 0 else courses(course=course['Section Name and Title'], all_emails=[])
        
        if ( not len(theCourse) or not len(theCourse.all_emails)):
            print('Starting process for ' + course['Section Name and Title'])
            sched.add_job(course_polling, 'interval', seconds=10, args=[ course['Section Name and Title'], sched ], id=course['Section Name and Title'])
            
        theCourse.save()
        theCourse.all_emails.append(theEmail)
        theCourse.save()
        
    return {"success": "true", "message":""}