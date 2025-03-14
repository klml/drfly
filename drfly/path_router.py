#!/usr/bin/env python
# coding: utf-8

import sys
import os
import argparse

import build_page
import config

def check_page_is_area(page_name, source_directory, cfg):

    # add dedicated spourcefile to the given pagename
    sourcefile  = os.path.realpath(source_directory) + os.path.sep + page_name
    areapath    = os.path.realpath(source_directory) + os.path.sep + cfg['directory']['area']

    # force to create all pages, if area is changed
    if areapath == os.path.commonpath([areapath, sourcefile]):
        return True

    return


def build_all(source_directory):

    cfg = config.config(source_directory)

    # iterate source directory and build all html and json files
    for dirName, subdirList, fileList in os.walk(os.path.realpath(source_directory), topdown=True):

        ## exclude directories
        [subdirList.remove(d) for d in list(subdirList) if d in cfg['sourceexclude']]
        [subdirList.remove(d) for d in list(subdirList) if d is cfg['template']]

        for filename in fileList:
            if (filename not in cfg['sourceexclude']):
                sourcefile = os.path.realpath(os.path.join(dirName, filename))
                result = build_page.build_html_json(sourcefile, source_directory, cfg)
                print(result) ## print here inside loop to get result while executing

    return


def build_single(page_name, source_directory):

    cfg = config.config(source_directory)

    if check_page_is_area(page_name, source_directory, cfg):
        build_all(source_directory)
        result = page_name + " is an area, so all pages were build"
    else:
        result = build_page.build_html_json(page_name, source_directory, cfg)

    return result
