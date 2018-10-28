from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.views.static import serve

import xadmin

from blog.views import (ArticleList, ArticleDetail, TagArticleList,
                        CatArticleList, sitemap, robot_txt, ClapRecordView, YXArticleList)


xadmin.autodiscover()

urlpatterns = [
    url(r'^$', ArticleList.as_view()),
    url(r'^/$', ArticleList.as_view()),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^yx/$', YXArticleList.as_view()),
    url(r'^articles/$', ArticleList.as_view()),
    url(r'^articles/(?P<article_id>[0-9]+)/$', ArticleDetail.as_view()),
    url(r'^tags/(?P<tag_id>[0-9]+)/articles', TagArticleList.as_view()),
    url(r'^category/(?P<cat_id>[0-9]+)/articles', CatArticleList.as_view()),
    url(r'^articles/clap/$', ClapRecordView.as_view()),
    url(r'xadmin/', include(xadmin.site.urls[:2])),
    url(r'sitemap/', sitemap),
    url(r'robots.txt/', robot_txt),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
