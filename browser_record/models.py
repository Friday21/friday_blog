# coding: utf-8
from django.db import models


class WebType(models.Model):
    type = models.CharField(max_length=32, verbose_name='网站类型')

    def __unicode__(self):
        return self.type


class Domain(models.Model):
    domain = models.CharField(max_length=64, verbose_name='网站')
    type = models.ForeignKey(WebType, verbose_name='网站类型', null=True, blank=True, on_delete=models.CASCADE)
    visit_count = models.IntegerField(verbose_name='访问次数', default=0, blank=True)
    last_visited_time = models.DateTimeField(verbose_name='最后访问时间', null=True, blank=True)

    def __unicode__(self):
        return self.domain


class ChromeRecord(models.Model):
    visit_time = models.DateTimeField(verbose_name='浏览时间')
    url = models.CharField(max_length=256, verbose_name='url')
    title = models.CharField(max_length=64, verbose_name='title')
    domain = models.ForeignKey(Domain, verbose_name='域名', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-visit_time']
