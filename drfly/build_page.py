#!/usr/bin/env python
# coding: utf-8

import json
import pystache
import os
import sys
import codecs

import markdown
from markdown.extensions import Extension

import config
import proserial
import get_meta
import get_area
import path_router


def render_prose_to_html(sourcefile, cfg, proserialsplit):

    # render markdown to html pages and json.
    if (os.path.splitext(sourcefile)[1] == '.md'):

        md = markdown.Markdown(
            extensions = cfg['markdown']['extensions'],
            extension_configs = cfg['markdown']['extension_configs']
            )
        return md.convert(proserialsplit[0])

    else:
        # txt-files get rendered with newlines as breaks (```<br>```).
        return proserialsplit[0].replace('\n','<br>\n')


def render_html_into_template(source_directory, tmplData):

    result = []

    if (tmplData['meta']['publish']):

        renderer = pystache.Renderer()

        html_html = renderer.render_path(source_directory + os.sep + tmplData['meta']['template'], tmplData)

        html_path = tmplData['meta']['directory']['html'] + os.sep + tmplData['content']['slugs']['html']

        html_file = codecs.open(html_path, 'w', encoding="utf-8")
        html_file.write(html_html)
        html_file.close()
        result.extend([html_path])


        json_json = json.dumps(tmplData)
        json_path = tmplData['meta']['directory']['html'] + os.sep + tmplData['content']['slugs']['json']
        json_file = codecs.open(json_path, 'w', encoding="utf-8")
        json_file.write(json_json)
        json_file.close()
        result.extend([json_path])

        result = json.dumps(result)

    return result


def build_html_json(sourcefile_path, source_directory, cfg):

    if not os.path.isfile(sourcefile_path) :
        return [sourcefile_path + ' does not exist']

    ## prevent directory traversal attack like ../../../index.md
    source_directory_realpath = os.path.realpath(source_directory)
    if os.path.commonprefix((os.path.realpath(sourcefile_path), source_directory_realpath)) == source_directory_realpath :

        proserialsplit                         = proserial.splitproseserial(sourcefile_path, cfg['separator'])
        if not proserialsplit :
            return [sourcefile_path + ' is not a text file']

        meta                                    = {**cfg} ## merge cfg into meta
        meta                                    = get_meta.get_meta_tree(sourcefile_path, source_directory_realpath, meta)
        meta                                    = get_meta.get_meta_file(sourcefile_path, proserialsplit, meta)
        meta_path                               = source_directory_realpath + os.sep + meta['directory']['area']

        # template data
        tmplData = {}
        tmplData['meta']                        = get_meta.get_html_title_from_first_heading(proserialsplit, meta)
        tmplData['content']                     = get_area.get_areas(meta_path, meta['sourceexclude'], meta['markdown'], cfg)
        tmplData['content']['slugs']            = get_meta.get_slugs(sourcefile_path, source_directory_realpath, meta['namespaceseparator'])
        tmplData['content']['source_git_meta']  = get_meta.get_source_git_meta(sourcefile_path, source_directory, meta['source_git_meta'] )

        tmplData['content']['main']             = render_prose_to_html(sourcefile_path, meta, proserialsplit)
        return render_html_into_template(source_directory, tmplData)

    else:
        return [sourcefile_path +  ' is an illegal path']