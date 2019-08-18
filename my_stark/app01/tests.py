from django.test import TestCase

# Create your tests here.
# Create your tests here.
def test(v1, *args, **kwargs):
    print(args, kwargs)


test(2,b=2,c=3)