# coding: utf-8
import xadmin

from .models import WebType, Domain, ChromeRecord
from blog_django.tools.time_process import get_local_format_time


class ChromeRecordAdmin(object):
    list_display = ['visit_date', 'web_url', 'web_title', 'type']
    list_filter = ['visit_time', 'domain']

    def type(self, obj):
        if obj.domain:
            return obj.domain.type
        return ''

    type.short_description = '网站类型'

    def visit_date(self, obj):
        return get_local_format_time(obj.visit_time)
    visit_date.short_description = '访问时间'

    def web_url(self, obj):
        return obj.url[:60]
    web_url.short_description = 'url'

    def web_title(self, obj):
        return obj.title[:35]
    web_title.short_description = 'title'


class DomainAdmin(object):
    list_display = ['domain', 'type', 'visit_count', 'last_visited_date']

    def last_visited_date(self, obj):
        if obj.last_visited_time:
            return get_local_format_time(obj.last_visited_time)
        return ''

    last_visited_date.short_description = '最后一次访问时间'


class WebTypeAdmin(object):
    list_display = ['type']


xadmin.site.register(ChromeRecord, ChromeRecordAdmin)
xadmin.site.register(Domain, DomainAdmin)
xadmin.site.register(WebType, WebTypeAdmin)
