# -*- coding: utf-8 -*-

import logging
import sqlite3
import re
from datetime import datetime, timedelta
from pytz import utc

from django.core.management.base import BaseCommand

from browser_record.models import Domain, ChromeRecord


logger = logging.getLogger(__name__)

history_db = '/root/myblog/files/History'
# history_db = '/home/friday/git/History'


class Command(BaseCommand):
    def handle(self, *args, **options):
        con = sqlite3.connect(history_db)
        cu = con.cursor()
        last_record = ChromeRecord.objects.first()
        last_record_time = last_record.visit_time if last_record else (datetime.now() - timedelta(days=30)).replace(tzinfo=utc)
        results = self.get_100_record(cu)
        offset = 0
        while results:
            for record in results:
                visit_time, url, title = record
                try:
                    url = url[:250]
                    title = title[:30]
                except:
                    url = 'wrong'
                    title = 'wrong'
                visit_time = datetime.strptime(visit_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=utc)
                if visit_time > datetime.now().replace(tzinfo=utc, hour=16, minute=0)-timedelta(days=1):
                    continue
                domain = re.findall('http[s]://(.*?)[/?]', url)
                if domain:
                    domain = domain[0]
                    if domain.count('.') > 1:
                        domain = domain[domain.index('.')+1:]
                    domain = Domain.objects.get_or_create(domain=domain)[0]
                    domain.visit_count += 1
                    domain.last_visited_time = visit_time
                    domain.save()
                chrome_record = ChromeRecord.objects.get_or_create(
                    visit_time=visit_time,
                    url=url,
                    title=title)[0]
                if domain:
                    chrome_record.domain = domain
                    chrome_record.save()
                print('save one')
            if visit_time <= last_record_time:
                break
            offset += 100
            results = self.get_100_record(cu, offset=offset)

    def get_100_record(self, cu, offset=0):
        sql = """select datetime(last_visit_time/1000000-11644473600, "unixepoch") as last_visited, url, title 
                        From urls order by last_visited desc limit 100 offset %s""" % offset
        cu.execute(sql)
        results = cu.fetchall()
        return results


