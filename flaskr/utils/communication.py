import yagmail
import datetime

class Communication:
    def __init__(self):
        self.yag = yagmail.SMTP()
        self.subject='Course Alert for {course}'
        self.content='''
                Hey!
                
                This is Guelph Alerts. Your course section {course} recently had space
                open up at {time}. Go grab it quickly before it is taken!
                
                Best of luck,
                Guelph Alerts
                '''
        
    def sendEmail(self, emails = None, course = None):
        curr_time = datetime.now().strftime("%I:%M:%S %p")
        self.yag.send(email, 
                      self.subject.format(course=course), 
                      self.content.format(course=course, time=curr_time))
    
    def initEmail(self, email):
        self.yag.send(email, 
                      "Successfully Monitoring!", 
                      '''
                      Hey!
                      
                      This is Guelph Alerts, just wanted to let you know that your courses are successfully being monitored!
                      When we find spots have opened in your courses, you'll be emailed as soon as possible!
                      
                      Cheers,
                      Guelph Alerts
                      ''')
    
    def text():
        pass