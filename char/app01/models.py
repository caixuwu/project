from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class user_info(AbstractUser):
    """
    用户表
    """
    username = models.CharField(max_length=20,unique=True)
    friend = models.ManyToManyField('self', related_name='my_friends', blank=True)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    class Meta:
        # 1,修改当前表名为User
        db_table = 'User'
        #2，修改实体类在后台管理页中的名称（单数）
        verbose_name = '用户'
        #3，修改实体类在后台管理页中的名称（复数）
        verbose_name_plural = verbose_name
        # 4，按照名字降序排序，可以指定按照年龄排序，再按照名字，或者再多的字段排序。
        ordering = ['-username']

class group(models.Model):
    '''
    群组表
    '''
    group_name = models.CharField(max_length=64,verbose_name='群名')
    owner = models.ForeignKey(user_info, None,verbose_name='创建者')
    admins = models.ManyToManyField(user_info, blank=True, related_name='group_admins',verbose_name='管理员')
    members = models.ManyToManyField(user_info, blank=True, related_name='group_members',verbose_name='成员')

    def __str__(self):
        return self.group_name

    class Meta:
        db_table='Group'
        verbose_name = '群组'
        verbose_name_plural = verbose_name
