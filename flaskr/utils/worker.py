from db import (courses, emails)
from uog import webadvisorQuery
from communication import Communication


def course_polling(course_title, sched):
    comm = Communication()

    searchable = course_title.split(') ')
    
    theCourse = courses.objects(course__in=[course_title])
    theCourse = theCourse[0] if len(theCourse) > 0 else theCourse
    
    if ( not len(theCourse) or not len(theCourse.all_emails)):
        print('Removing process for ' + course_title)
        sched.remove_job(course_title)
        
    all_courses = webadvisorQuery({'VAR1': 'F20' ,'VAR3': searchable[1], 'VAR6':'G'})
        
    found = None
    for course in all_courses['data'].values():
        if course['Section Name and Title'] == course_title:
            found = course
            break
        
    if found:
        cap = int(found['Available/ Capacity'].split('/')[0])
        if( cap > 0 ):
            emails = [email.email for email in theCourse.all_emails]
            comm.sendEmail(emails , course_title)
            theCourse.delete()
            
