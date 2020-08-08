from db import emails
from datetime import (datetime, timedelta)

def cleanup_email():
    print('Removing expired emails....')
    todays_date = datetime.utcnow()
    emails.objects(expire__in=[todays_date.strftime('%Y-%m-%d')]).delete()