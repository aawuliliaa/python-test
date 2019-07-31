from django.test import TestCase

# Create your tests here.
from testchannel.tasks import *
if __name__ == '__main__':
    # tailf.delay(1,"wewe")
    t = add.delay()
    # print(t.get())