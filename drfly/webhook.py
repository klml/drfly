#!/usr/bin/env python3.6
# coding: utf-8
import os, sys, git

# depending http://webpy.org
import web

import config
import build_page
import build_all_pages
import gitpull


urls = (
    '/gitpull',         'git_pull',
    '/render',          'render'
)
app = web.application(urls, globals())

# set source_directory
# disallow changing source directory from web
source_directory = sys.argv[2]
cfg = config.config(source_directory)


class git_pull:
    def POST(self):
        if cfg['webhook']['gitpull']:
            return gitpull.gitpull(source_directory)


class render:
    def GET(self):
        getparam    = web.input(_method='get')

        # https://example.com/render?page=
        if cfg['webhook']['render'] and 'page' in getparam :
            return build_page.check_page_is_area(getparam['page'], source_directory)

        # https://example.com/render?all
        if cfg['webhook']['renderall'] and 'all' in getparam :
            build_all_pages.build_all(source_directory)
            return "all pages rendered"


if __name__ == '__main__':
        app.run()

