#!/usr/bin/env python
# coding: utf-8

import sys, os
import build_page
import path_router

if __name__ == "__main__":

    source_directory    = os.getcwd()

    # if no parameter is given: render all pages
    if (len(sys.argv[1:]) == 0):
        path_router.build_all(source_directory)
        print('pages build') ## result is printed in drfly/build_all_pages.py

    else:
        for page_path in sys.argv[1:] :

            if os.path.isfile(page_path):
                print(path_router.check_page_is_area(page_path , source_directory))

            if os.path.isdir(page_path):
                path_router.build_all(page_path)
                print('pages build') ## result is printed in drfly/build_all_pages.py