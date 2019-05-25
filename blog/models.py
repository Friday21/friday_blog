# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/friday/friday_blog/blog_django/static/img')  # TODO 动态生成


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='目录')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='标签')

    def __str__(self):
        return self.name


class Article(models.Model):
    cat = models.ForeignKey(Category, default=None, verbose_name='目录', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, default=None, verbose_name='标签', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='文章标题')
    content = models.TextField(default='', verbose_name='文章内容')
    icon = models.ImageField(verbose_name='缩略图', null=True, blank=True)
    desc = models.CharField(max_length=255, verbose_name='引导语')
    perm_level = models.IntegerField(default=0, verbose_name='加密等级')
    view_count = models.IntegerField(default=0, verbose_name='浏览次数')
    event_date = models.DateTimeField(blank=True, verbose_name='发布时间')

    def save(self, *args, **kwargs):
        if not self.event_date:
            self.event_date = datetime.now()
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(verbose_name='图片')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.image.name


class LikeMe(models.Model):
    ip = models.CharField(max_length=255, verbose_name='IP')
    click_time = models.IntegerField(default=0, verbose_name='点击次数')
    like_time = models.DateTimeField(auto_now=True, verbose_name='like时间')


class AccessLog(models.Model):
    ip = models.CharField(max_length=64, verbose_name='IP')
    dev = models.CharField(max_length=64, null=True, verbose_name='设备')
    browser = models.CharField(max_length=255, null=True, verbose_name='浏览器')
    system = models.CharField(max_length=64, null=True, verbose_name='系统')
    ua = models.CharField(max_length=512, verbose_name='user-agent')
    url = models.CharField(max_length=255, verbose_name='访问网页')
    refer = models.CharField(max_length=255, verbose_name='HTTP_REFER')
    access_time = models.DateTimeField(verbose_name='访问时间')
    address = models.CharField(max_length=255, null=True, verbose_name='地址')
    memo = models.CharField(max_length=255, verbose_name='备注', null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    ip138 = models.CharField(max_length=255, null=True, verbose_name='ip138地址')
    fp2 = models.CharField(max_length=32, null=True, verbose_name='指纹')
    language = models.CharField(max_length=32, null=True, verbose_name='语言')
    resolution = models.CharField(max_length=32, null=True, verbose_name='分辨率')
    platform = models.CharField(max_length=32, null=True, verbose_name='系统平台')


class ClapRecord(models.Model):
    article = models.ForeignKey(Article, verbose_name='文章', on_delete=models.CASCADE)
    clapper = models.CharField(max_length=64, default='无名', verbose_name='鼓掌人')
    fp2 = models.CharField(max_length=64, default='', verbose_name='设备指纹')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']


class Song(models.Model):
    name = models.CharField(max_length=128, verbose_name='歌名')
    artist = models.CharField(max_length=128, verbose_name='歌手')
    sort = models.IntegerField(default=100, verbose_name='排名')
    song = models.FileField(verbose_name='文件', storage=fs)

    class Meta:
        ordering = ['sort']
