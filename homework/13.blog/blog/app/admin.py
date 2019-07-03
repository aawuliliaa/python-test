from django.contrib import admin

# Register your models here.


from app import models
# 这里是让自己新建的表在admin页面中出现，从而可以在admin页面添加数据
admin.site.register(models.UserInfo)
admin.site.register(models.Blog)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Article)
admin.site.register(models.ArticleUpDown)
admin.site.register(models.ArticleToTag)
admin.site.register(models.Comment)