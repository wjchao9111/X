from django.db import models
from base.models import User


class Form(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'名字')

    def __unicode__(self):
        return u'%s' % (self.name)


class Prop(models.Model):
    bool_choices = (('true', u'是'), ('false', u'否'),)
    type_choices = (('char', u'字符串'), ('text', u'文本'), ('int', u'整数'), ('float', u'小数'),
                    ('datetime', u'时间'), ('date', u'日期'), ('file', u'文件'), ('image', u'图片'),)
    form = models.ForeignKey(Form, verbose_name=u'表单')
    name = models.CharField(max_length=50, verbose_name=u'名字')
    type = models.CharField(max_length=50, choices=type_choices, verbose_name=u'类型')
    show = models.CharField(max_length=50, choices=bool_choices, default='true', verbose_name=u'是否显示')
    edit = models.CharField(max_length=50, choices=bool_choices, default='true', verbose_name=u'是否修改')
    default = models.CharField(max_length=50, verbose_name=u'默认值')
    choices = models.CharField(max_length=200, verbose_name=u'选项')
    regex = models.CharField(max_length=200, default=u'', verbose_name=u'正则表达式')
    blank = models.CharField(max_length=50, choices=bool_choices, default='false', verbose_name=u'允许空值')
    rank = models.IntegerField(default=0, verbose_name=u'排名')
    index = models.CharField(max_length=50, choices=bool_choices, default='false', verbose_name=u'索引')

    def __unicode__(self):
        return u'%s|%s' % (self.form.name, self.name)


class Row(models.Model):
    conf = models.ForeignKey(Form, verbose_name=u'表单类型')
    add_user = models.ForeignKey(User, verbose_name=u'创建用户')
    update_user = models.ForeignKey(User, verbose_name=u'创建用户')
    add_time = models.DateTimeField(verbose_name='创建时间')
    update_time = models.DateTimeField(verbose_name='修改时间')
    keyword = models.CharField(max_length=200, default=u'', db_index=True, verbose_name=u'关键字')

    def __unicode__(self):
        return u'%s' % self.keyword


class Field(models.Model):
    row = models.ForeignKey(Row, verbose_name=u'行号')
    prop = models.ForeignKey(Prop, verbose_name=u'属性')
    version = models.IntegerField(default=0, verbose_name=u'版本')
    user = models.ForeignKey(User, verbose_name=u'用户')
    time = models.DateTimeField(verbose_name='时间')
    text_value = models.TextField(null=True, blank=True, verbose_name=u'文本值')
    int_value = models.IntegerField(null=True, blank=True, verbose_name=u'整数值')
    float_value = models.FloatField(null=True, blank=True, verbose_name=u'小数值')
    datetime_value = models.DateTimeField(null=True, blank=True, verbose_name=u'时间值')
    date_value = models.DateField(null=True, blank=True, verbose_name=u'日期值')
    file_value = models.FileField(null=True, blank=True, verbose_name=u'文件值')
    image_value = models.ImageField(null=True, blank=True, verbose_name=u'图片值')

    def __unicode__(self):
        if self.text_value is not None:
            return self.text_value
        if self.int_value is not None:
            return self.int_value
        if self.float_value is not None:
            return self.float_value
        if self.datetime_value is not None:
            return self.datetime_value
        if self.date_value is not None:
            return self.date_value
        if self.file_value is not None:
            return self.file_value
        if self.image_value is not None:
            return self.image_value
