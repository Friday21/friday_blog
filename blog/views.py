# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, StreamingHttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from blog.models import Article, Tag, ClapRecord, AccessLog
from blog.api import get_article_info, get_cat_info_list, get_tag_info_list, get_articles_context
from blog_django.utils.mkdoc_build import render_content


class ArticleList(View):

    def get(self, request):
        article_list = Article.objects.filter(perm_level__lt=100).order_by('-event_date').all()
        page = int(request.GET.get('page', 1))
        context = get_articles_context(article_list, page)
        context.update({'home_page': True})
        return render(request, 'blog/article_list.html', context)

    def post(self, request):
        pass


class YXArticleList(View):

    def get(self, request):
        # 100 level 以上的是yx的article
        article_list = Article.objects.filter(perm_level__gte=100).order_by('-event_date').all()
        page = int(request.GET.get('page', 1))
        context = get_articles_context(article_list, page)
        context.update({'home_page': True})
        return render(request, 'blog/article_list.html', context)


class ArticleDetail(View):

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        article_info = get_article_info(article)
        article_title = article_info['title']
        page_content = article_info['content']
        pre_article = Article.objects.filter(id__lt=article_id).order_by('-id').first()
        pre_article_id = pre_article.id if pre_article else ''
        next_article = Article.objects.filter(id__gt=article_id).order_by('id').first()
        next_article_id = next_article.id if next_article else ''
        page_content = render_content(page_content, pre_article_id, next_article_id)
        clap_count = ClapRecord.objects.all().count()
        context = dict(article_id=article_id,
                       pre_article_id=pre_article_id, next_article_id=next_article_id,
                       article_title=article_title, cat_info_list=get_cat_info_list(),
                       tag_info_list=get_tag_info_list(), date=article_info['date'],
                       clap_count=clap_count,
                       page_url='/articles/{}/'.format(article_id),
                       page_identify='id_{}'.format(article_id))
        context.update(page_content)
        return render(request, 'mk_docs/main.html', context)

    def put(self, request):
        pass

    def delete(self, request):
        pass


class TagList(View):

    def get(self, request):
        tags = Tag.objects.all()
        tag_info = [{'id': tag.id, 'name': tag.name} for tag in tags]
        return JsonResponse(data=tag_info)

    def post(self, request):
        pass


class TagArticleList(View):

    def get(self, request, tag_id):
        articles = Article.objects.filter(tag_id=tag_id, perm_level__lt=100).order_by('-event_date')
        page = int(request.GET.get('page', 1))
        context = get_articles_context(articles, page)
        context.update({'home_page': False})
        return render(request, 'blog/article_list.html', context)


class CatArticleList(View):

    def get(self, request, cat_id):
        articles = Article.objects.filter(cat_id=cat_id, perm_level__lt=100).order_by('-event_date')
        page = int(request.GET.get('page', 1))
        context = get_articles_context(articles, page)
        context.update({'home_page': False})
        return render(request, 'blog/article_list.html', context)


def sitemap(request):
    content = ['http://www.fridayhaohao.com/']
    for id in Article.objects.values_list('id', flat=True):
        content.append('http://www.fridayhaohao.com/articles/{}/'.format(id))
    content = '\n'.join(content)
    the_file_name = "sitemap.txt"
    response = StreamingHttpResponse(content)
    response['Content-Type'] = 'txt/csv'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response


def robot_txt(request):
    content = """User-agent: *
Disallow: /admin*
Disallow: /xadmin*
Sitemap: http://www.fridayhaohao.com/sitemap"""
    the_file_name = "robots.txt"
    response = StreamingHttpResponse(content)
    response['Content-Type'] = 'txt/csv'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response


class ClapRecordView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ClapRecordView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        fp2 = request.POST.get('fp2')
        from_url = request.POST.get('from_url')
        clappers = AccessLog.objects.filter(fp2=fp2, memo__isnull=False).first()
        if clappers:
            clapper = clappers.memo.replace('fp:', '') or '无名'
        else:
            clapper = '无名'
        if '李东勇' in clapper:
            return JsonResponse(data={'msg': '自己鼓掌可不算哦'})
        article_id = re.findall('/articles/([0-9]+)/', from_url)
        if not article_id:
            return JsonResponse(data={'msg': 'article not found'})
        article_id = int(article_id[0])
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return JsonResponse(data={'msg': 'article not found, article_id:{}'.format(article_id)})
        clap_record = ClapRecord(
            article=article,
            clapper=clapper,
            fp2=fp2,
        )
        clap_record.save()
        return JsonResponse(data={'msg': 'success'})