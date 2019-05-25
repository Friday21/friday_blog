# encoding: utf-8
from __future__ import unicode_literals

import xadmin
from datetime import datetime

from django.utils.timezone import localtime
from xadmin.filters import ChoicesFieldListFilter, manager

from blog.models import Article, Category, Tag, Image, AccessLog, ClapRecord, Song


class UrlFilter(ChoicesFieldListFilter):

    def __init__(self, field, request, params, model, admin_view, field_path):
        super(UrlFilter, self).__init__(field, request, params, model, admin_view, field_path)
        self.title = '过滤url'

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'url'

    def choices(self):
        values = ('非/', '全部')
        for url in values:
            yield {
                'selected': url == self.lookup_exact_val,
                'query_string': self.query_string({self.lookup_exact_name: url}),
                'display': url,
            }

    def do_filte(self, queryset):
        if 'url__exact' in self.used_params:
            visit_page = self.used_params['url__exact'].strip()
            if visit_page == '非/':
                return queryset.exclude(url=' / ')
            else:
                return queryset
        return queryset.filter(**self.used_params)
manager.register(UrlFilter, take_priority=True)


class ArticleAdmin(object):
    list_display = ['id', 'cat', 'tag', 'titles', 'desc',
                    'icon_url', 'view_count', 'event_date']
    list_display_links = ['id']

    def icon_url(self, obj):
        return '<img src="%s" height=50/>' % obj.icon.url

    icon_url.allow_tags = True
    icon_url.short_description = '缩略图'

    def titles(self, obj):
        return """
        <a href=/articles/%s/>%s</a>""" % (obj.id, obj.title)

    titles.allow_tags = True
    titles.short_description = '文章标题'


class ImageAdmin(object):
    list_display = ['id', 'pic', 'markdown_code', 'create_date']

    def pic(self, obj):
        return '<img src="%s" height=50/>' % obj.image.url

    pic.allow_tags = True
    pic.short_description = '图片'

    def markdown_code(self, obj):
        return '![描述](%s)' % obj.image.url

    markdown_code.allow_tags = True
    markdown_code.short_description = 'markdown code'


class TagAdmin(object):
    list_display = ['id', 'name']


class CategoryAdmin(object):
    list_display = ['id', 'name']


class AccessLogAdmin(object):
    list_display = ['dev', 'browser', 'address138', 'url', 'language', 'resolution', 'memo', 'access_date']
    list_editable = ['memo']
    list_filter = ['memo', 'access_time', 'dev', 'url', 'fp2']
    search_fields = ['memo', 'address']
    show_detail_fields = ['dev']

    def address138(self, obj):
        if obj.address and obj.ip138:
            return obj.address + obj.ip138
        elif obj.address:
            return obj.address
        else:
            return obj.ip138

    address138.allow_tags = True
    address138.short_description = '地址'

    def access_date(self, obj):
        return datetime.strftime(localtime(obj.access_time), '%Y-%m-%d %H:%M')

    access_date.allow_tags = True
    access_date.short_description = '访问时间'


class ClapRecordAdmin(object):
    list_display = ['clapper', 'article', 'clap_time']

    def clap_time(self, obj):
        return datetime.strftime(localtime(obj.created_time), '%Y-%m-%d %H:%M')


class SongAdmin(object):
    list_display = ['id', 'name', 'artist', 'url', 'sort']


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Image, ImageAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(AccessLog, AccessLogAdmin)
xadmin.site.register(ClapRecord, ClapRecordAdmin)
xadmin.site.register(Song, SongAdmin)
