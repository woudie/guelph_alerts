from flaskr.utils.communication import Communication
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

class Scheduler:
    def __init__(self):
        self.comm = Communication()
        
    def addJob(self, func, time):
        pass
    
    