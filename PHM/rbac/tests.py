from django.test import TestCase
li = [{"tile":"wewe"}]
# Create your tests here.
li[0]["tile"] = "new"
print(li)  # [{'tile': 'new'}]
