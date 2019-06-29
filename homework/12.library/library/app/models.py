from django.db import models

# Create your models here.


class Author(models.Model):
    # 作者表
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    age = models.IntegerField()


class Publish(models.Model):
    # 出版社表
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    email = models.EmailField()


class Book(models.Model):
    # 图书表
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    publishDate = models.DateField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    # 书籍与出版社是多对一
    publish = models.ForeignKey(to_field="id", to="Publish", on_delete=models.CASCADE)
    # 书籍与作者关系是多对多
    authors = models.ManyToManyField(to="Author")
