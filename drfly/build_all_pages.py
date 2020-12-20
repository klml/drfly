#!/usr/bin/env python
# coding: utf-8

import sys
import os
import argparse

import build_page
import config


def build_all(source_directory):

    cfg = config.config(source_directory)
    source_directory_realpath = os.path.realpath(source_directory)

    # iterate source directory and build all html and json files
    for dirName, subdirList, fileList in os.walk(source_directory_realpath , topdown=True):

        ## exclude directories
        [subdirList.remove(d) for d in list(subdirList) if d in cfg['sourceexclude'] ]
        [subdirList.remove(d) for d in list(subdirList) if d is cfg['template'] ]

        for filename in fileList:
            if (filename not in cfg['sourceexclude']):
                sourcefile = os.path.realpath(os.path.join(dirName, filename))
                result = build_page.build_html_json(sourcefile, source_directory)
                print(result) ## print here inside loop to get result while executing

    return result

if __name__ == "__main__":
    build_all(os.getcwd())

