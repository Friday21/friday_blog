# encoding: utf-8

from collections import namedtuple
from copy import deepcopy

import xadmin
from xadmin import views


class BaseSetting(object):
    enable_themes = False
    use_bootswatch = True

    def block_extrahead(self, context, nodes):
        return """<link rel="shortcut icon" 
href="/static/img/159daa56cdf603b3404fcdfcbfd701b81274.PNG)"/>"""  # noqa


class GlobeSetting(object):
    site_title = '我的精神家园'
    site_footer = 'powered by 李东勇'
    # menu_style = "accordion"


class NavMenuPlugin(views.BaseAdminPlugin):
    MenuBlock = namedtuple('MenuBlock', 'title items')
    MenuItem = namedtuple('MenuItem', 'title name icon url app')
    MenuItemReplace = namedtuple('MenuItem', 'perm title')
    target_menu = [
        MenuBlock('计划', [
            MenuItemReplace('plan.view_dailyplan', '日计划',),
            MenuItemReplace('plan.view_weekplan', '周计划',),
            MenuItemReplace('plan.view_monthplan', '月计划',),
            MenuItemReplace('plan.view_yearplan', '年计划',),
            MenuItemReplace('plan.view_eventtype', '事件类型',),
        ]),

        MenuBlock('浏览记录', [
            MenuItemReplace('browser_record.view_chromerecord', '上网记录', ),
            MenuItemReplace('browser_record.view_domain', '浏览网站', ),
            MenuItemReplace('browser_record.view_webtype', '网站类型', ),
        ]),

        MenuBlock('财务', [
            MenuItemReplace('bill.view_balancelog', '消费记录', ),
            MenuItemReplace('bill.view_consumetype', '消费类型', ),
        ]),

        MenuBlock('博客', [
            MenuItemReplace('blog.view_accesslog', '访客记录', ),
            MenuItemReplace('blog.view_claprecord', '鼓掌记录', ),
            MenuItemReplace('blog.view_article', '博客文章'),
            MenuItemReplace('blog.view_image', '图片'),
            MenuItemReplace('blog.view_tag', '标签'),
            MenuItemReplace('blog.view_category', '目录', ),
        ]),
    ]

    def get_nav_menu(self, navi_menu):
        menu_map = {}
        for block in navi_menu:
            for menu in block['menus']:
                menu_map[menu['perm']] = menu

        result_menu = []
        for block in self.target_menu:
            block_menu = {
                'title': block.title,
                'first_url': '',
                'menus': []
            }

            for item in block.items:
                if isinstance(item, self.MenuItem):
                    item_menu = {
                        'perm': '%s.%s' % (item.app, item.name),
                        'title': item.title,
                        'url': item.url,
                        'icon': item.icon,
                    }
                elif isinstance(item, self.MenuItemReplace):
                    item_menu = deepcopy(menu_map[item.perm])
                    item_menu['title'] = item.title
                else:
                    item_menu = menu_map[item]

                block_menu['menus'].append(item_menu)
            result_menu.append(block_menu)
        return result_menu


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobeSetting)
xadmin.site.register_plugin(NavMenuPlugin, views.CommAdminView)
