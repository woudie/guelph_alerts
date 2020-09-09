import os
from flask import (Flask, render_template, json)
from flask_mongoengine import MongoEngine
from . import (courses, home, cart)
from utils.scheduler import Scheduler

def create_app(test_config=None):
    db = MongoEngine()
    db_uri = "mongodb+srv://{user}:{passw}@cluster0-czbyg.mongodb.net/GuelphAlerts?retryWrites=true&w=majority"
    
    sched = Scheduler()
    if Scheduler.sched == None:
        sched.startScheduler()
        sched = Scheduler.sched

    
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.config['MONGODB_SETTINGS'] = {
        'db': 'GuelphAlerts',
        'host': db_uri.format(user=os.environ['DB_USERNAME'], passw=os.environ['DB_PASSWORD'])
    }
    
    db.init_app(app)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(home.bp)
    app.register_blueprint(courses.courses_bp)
    app.register_blueprint(cart.bp)
    
    sched.initScheduler()
    
    return app