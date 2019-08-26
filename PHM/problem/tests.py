from django.test import TestCase
import datetime
import time
# Create your tests here.
start = datetime.datetime.now()

time.sleep(5)
stop = datetime.datetime.now()
timeqq = stop -start
print(timeqq.seconds/60)
