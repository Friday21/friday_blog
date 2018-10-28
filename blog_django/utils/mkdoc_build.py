# encoding: utf-8
import re

from mkdocs.commands.build import nav, convert_markdown, get_global_context, get_page_context
from mkdocs.config import load_config
from django.conf import settings


def render_content(input_content, pre_article_id, next_article_id):
    input_content = input_content.replace('\r\n', '    \r\n')
    config = load_config(
        config_file=settings.BASE_DIR + '/blog_django/utils/mkdocs.yml',
        docs_dir=settings.BASE_DIR + '/blog_django/utils/docs',
    )
    site_navigation = nav.SiteNavigation(config['pages'], config['use_directory_urls'])
    for page in site_navigation.walk_pages():
        pass
    # Process the markdown text
    html_content, table_of_contents, meta = convert_markdown(
        markdown_source=input_content,
        config=config,
        site_navigation=site_navigation
    )

    html_content = html_content.replace('src="./', 'src="/')
    # 添加视频

    html_content = re.sub("(?P<video><p>@video_start@.*?@video_end@</p>)", sub_video, html_content)

    context = get_global_context(site_navigation, config)
    context['base_url'] = '/static/mk_docs'
    context.update(get_page_context(
        page, html_content, table_of_contents, meta, config
    ))
    context['page'].next_article_id = next_article_id
    context['page'].pre_article_id = pre_article_id

    return context


def sub_video(video):
    video = video.group('video')
    video_link = video.replace('<p>@video_start@', '').replace('@video_end@</p>', '')
    return """<iframe width="560" height="315" src="{}" 
    frameborder="0" allow="autoplay; encrypted-media" allowfullscreen>
    </iframe>""".format(video_link)