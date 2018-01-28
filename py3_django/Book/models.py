from django.db import models


# Create your models here.
# 准备书籍列表信息的模型类
class BookInfo(models.Model):
    # 创建字段，字段类型...
    name = models.CharField(max_length=10)

    def __str__(self):
        # py2需要编码py3不需要
        # return self.name.encode('utf-8')
        return self.name

# 准备人物列表信息的模型类
class PeopleInfo(models.Model):
    name = models.CharField(max_length=10)
    gender = models.BooleanField()
    # 外键约束：人物属于哪本书
    book = models.ForeignKey(BookInfo)

    def __str__(self):
        return self.name
