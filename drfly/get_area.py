#!/usr/bin/env python
# coding: utf-8

import os
import codecs
import markdown

def get_areas(config_directory_area, config_sourceexclude, config_markdown, cfg):

    ## areas
    # include sourcefiles as  in templates (for menus, sidebars, trackingpixels).

    areas = {}
    for dirName, subdirList, fileList in os.walk(config_directory_area):
        ## exclude directories
        [subdirList.remove(d) for d in list(subdirList) if d in config_sourceexclude]

        for filename in fileList:
            with codecs.open(os.path.join(dirName, filename), 'r', encoding="utf-8") as openareafile:
                areamd = openareafile.read()

            md = markdown.Markdown(
                extensions= config_markdown['area_extensions'],
                extension_configs = cfg['markdown']['extension_configs']
                )
            areahtml = md.convert(areamd)

            areas[os.path.splitext(filename)[0]] = areahtml

    return areas

