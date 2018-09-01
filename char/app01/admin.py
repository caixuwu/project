from django.contrib import admin
from app01 import models
# Register your models here.

#声明高级管理类
class UserAdmin(admin.ModelAdmin):
    #1,指定显示的字段
    list_display = ('username','email','is_active')
    #2,指定能链接到详情页的字段们
    list_display_links = ['username','email']
    #3,指定在列表页中就允许修改的字段们
    list_editable = ['is_active']
    #4,添加允许被搜索的字段们
    search_fields = ['last_login','data_joined']
    #5,在列表也的右侧增加过滤器，实现快速筛选
    list_filter = ['username']
    #6,在列表页顶部增加时间选择器，所有取值必须是DateField 或 DateTimeField 的列
    # date_hierarchy = '必须是datafile类型'
    #7，在详情页面中，指定显示哪些字段并按照什么样的顺序显示
    # fields = ['username','password','is_active']
    #8,在详情页面中，对字段们进行分组显示
    fieldsets = (
        (
            '基本信息',{
                'fields':('username','email'),
            }
        ),
        (
            '可选信息',{
              'fields':('last_login',),
                'classes':('collapse',)
            }
        )
    )


class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_name']




admin.site.register(models.user_info,UserAdmin)
admin.site.register(models.group,GroupAdmin)

