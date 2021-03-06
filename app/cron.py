from datetime import datetime as dt, timezone
from .models import Polls

def pollstopper():
    print("crontab exec", dt.now())
    try:
        polls = Polls.objects.all()
        print("Polls found", dt.now())
        for poll in polls:
            bal = dt.now(timezone.utc) - poll.timestamp
            print("bal",bal)
            if bal.days >= 1:
                poll.completed = True
                poll.save()
                print("Crontab task executed id: %s"%(poll.id))
        print("==========================================================================")
    except Exception as e:
        print(e)
                 

