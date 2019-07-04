from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户信息
    """
    id = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    # 该字段存放的是用户头像的路径
    avatar = models.FileField(upload_to="avatars/", default="avatars/default.png")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    blog = models.OneToOneField(to="Blog", to_field="id", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Blog(models.Model):
    """
    个人博客信息
    账户信息与博客是一对一的关系，每个人只有一个站点页面，一个站点页面只属于一个用户
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="个人博客标题", max_length=64)
    site_name = models.CharField(verbose_name="个人站点名称", max_length=64)
    theme = models.CharField(verbose_name="博客主体", max_length=32)

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    文章分类表
    一个个人站点有多个文章分类，一个分类只属于一个用户
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="分类名称", max_length=32)
    blog = models.ForeignKey(verbose_name="所属博客", to_field="id", to="Blog", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    标签种类
    一个用户的博客站点有多个标签，一个标签属于一个个人站点
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="标签名称", max_length=32)
    blog = models.ForeignKey(verbose_name="所属的博客", to="Blog", to_field="id", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Article(models.Model):
    """
    文章表
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="文章标题", max_length=50)
    desc = models.CharField(verbose_name="文章描述", max_length=255)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    content = models.TextField()
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(verbose_name="点赞数", default=0)
    down_count = models.IntegerField(verbose_name="反对数", default=0)

    user = models.ForeignKey(verbose_name="作者", to="UserInfo", to_field="id", on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name="所属分类", to="Category", to_field="id", on_delete=models.CASCADE)
    tags = models.ManyToManyField(verbose_name="所属标签", to="Tag", through="ArticleToTag")


class ArticleToTag(models.Model):
    """
    文章和标签的中间关联表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="id", on_delete=models.CASCADE, verbose_name="关联的文章")
    tag = models.ForeignKey(to="Tag", to_field="id", on_delete=models.CASCADE, verbose_name="关联的标签")

    class Meta:
        # 设置联合主键
        unique_together = [
            ('article', 'tag'),
        ]

    def __str__(self):
        return self.article.title+"_"+self.tag.title


class ArticleUpDown(models.Model):
    """
    点赞表，这里主要是页面中要判断某用户对某文章是否点赞过，如果点赞过，就提示不需要点赞了
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", to_field="id", on_delete=models.CASCADE, verbose_name="所属用户")
    article = models.ForeignKey(to="Article", to_field="id", on_delete=models.CASCADE, verbose_name="所属文章")
    is_up = models.BooleanField(default=True, verbose_name="赞为True，反对为False")

    class Meta:
        unique_together = [("user", "article")]


class Comment(models.Model):
    """
    评论表,
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", to_field="id", on_delete=models.CASCADE, verbose_name="所属用户")
    article = models.ForeignKey(to="Article", to_field="id", on_delete=models.CASCADE, verbose_name="所属文章")
    content = models.CharField(verbose_name="评论内容", max_length=255)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    parent_comment = models.ForeignKey("self", null=True, on_delete=models.CASCADE, verbose_name="父评论的id")

    def __str__(self):
        return self.content
