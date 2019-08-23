from django.test import TestCase
li = [{"title":"wewe"}]
dict = {"1":li[0]}
dict["1"]["title"]="new"
print(li)  # [{'tile': 'new'}]
