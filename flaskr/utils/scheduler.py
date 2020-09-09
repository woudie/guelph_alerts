from flaskr.utils.communication import Communication
from apscheduler.schedulers.background import BackgroundScheduler
from db import (courses, emails)
from worker import course_polling
import json

class Scheduler:
    sched = None
    
    def __init__(self):
        self.comm = Communication()
    
    def startScheduler(self):
        Scheduler.sched = BackgroundScheduler(daemon=True)
        Scheduler.sched.start()

    
    def initScheduler(self):
        found = courses.objects().scalar('course')
        
        for course in found:
            if Scheduler.sched.get_job(course) == None:
                print('Starting process for ' + course)
                Scheduler.sched.add_job(course_polling, 'interval', seconds=10, args=[ course, Scheduler.sched ], id=course)
            
        
    
    