# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from blog.models import Tag, Category


def get_articles_context(article_list, page):
    article_info_list = []
    page_num = (len(article_list) - 6) // 9 + 2 if len(article_list) > 6 else 1
    if page > page_num:
        page = page_num
    next_page = page + 1 if page < page_num else False
    pre_page = page - 1 if page > 1 else False
    pages = list()
    page_start = page - page % 5 + 1 if page % 5 != 0 else page - page % 5 - 4
    page_end = page - page % 5 + 7 if (page - page % 5 + 7) < page_num + 1 else page_num + 1
    for i in range(page_start, page_end):
        pages.append(dict(active=0, page_num=i))
    pages[page - page_start]['active'] = 1
    article_list = article_list[9 * (page - 2) + 6:9 * (page - 1) + 6] if page > 1 else article_list[:6]
    cnt = 1
    for article in article_list:
        article_info = get_article_info(article)
        article_info['cnt'] = cnt
        cnt = cnt % 3 + 1
        article_info_list.append(article_info)
    context = {'article_info_list': article_info_list, 'pages': pages, 'page_num': page,
               'cat_info_list': get_cat_info_list(), 'tag_info_list': get_tag_info_list(),
               'next_page': next_page, 'pre_page': pre_page}
    return context


def get_article_info(article):
    title = article.title
    desc = article.desc
    desc_length = char_len(desc)
    if desc_length < 88:
        desc += '*'*88
    if char_len(title) > 16:
        title = title[:16]
    if char_len(title) > 8:
        new_desc = desc[:68]
        while char_len(new_desc) < 68:
            new_desc += desc[len(new_desc)]
    else:
        new_desc = desc[:82]
        while char_len(new_desc) < 82:
            new_desc += desc[len(new_desc)]
    article_info = dict(title=title, id=article.id, cat_id=article.cat_id,
                        tag_id=article.tag_id, description=new_desc,
                        content=article.content, perm_level=article.perm_level,
                        icon_url=article.icon.url, cat_name=article.cat.name,
                        tag_name=article.tag.name, date=article.event_date.strftime('%y-%m-%d'))
    return article_info


def get_tag_info_list():
    tags = Tag.objects.all()
    tag_info_list = list()
    for tag in tags:
        tag_info_list.append(dict(id=tag.id, name=tag.name))
    return tag_info_list


def get_cat_info_list():
    cats = Category.objects.all()
    cat_info_list = list()
    for cat in cats:
        cat_info_list.append(dict(id=cat.id, name=cat.name))
    return cat_info_list


def char_len(data):
    chinese_char = re.findall(r'[\u4e00-\u9fff]', data)
    char_count = len(data)
    chinese_char_count = len(chinese_char) + data.count(' ')
    non_chinese_char_count = char_count - chinese_char_count
    char_length = chinese_char_count + (0.5 * non_chinese_char_count)
    return char_length
