#!/usr/bin/env python
# coding: utf-8

import os
import yaml
import time
import re
import git


## load serial data
def get_meta_tree(sourcefile, source_directory_realpath, meta):

    ## collect meta
    # get metadata from file meta.yaml in every directory in sourcepath

    stepsourcedir = ''
    for index, directory in enumerate(os.path.dirname(sourcefile).split(os.sep)):

        stepsourcedir += directory + os.sep

        ## avoid searching for yaml "under" source_directory
        if os.path.commonprefix((stepsourcedir, source_directory_realpath)) == source_directory_realpath:

            ## define meta file
            # [Please use ".yaml" when possible.](https://yaml.org/faq.html)
            meta_directory_file = stepsourcedir + 'meta.yaml'

            # Check if the metafile exists
            if (os.path.isfile(meta_directory_file)):

                with open(meta_directory_file, 'r') as openmeta_directory_file:
                    meta_directory = openmeta_directory_file.read()
                meta.update(yaml.load(meta_directory, Loader=yaml.FullLoader))
    return meta


def get_meta_file(sourcefile, proserial, meta):
    ## check if source file includes metadata
    try:
        proserial_meta = yaml.load(proserial[1], Loader=yaml.FullLoader)
        meta.update(proserial_meta)
        return meta

    ## sourcefile-meta is no valid yaml
    ## or
    ## sourcefile-meta does not exists
    ## this is PROSErial conform
    ## TODO warn user
    except:
        return meta


def get_html_title_from_first_heading(proserial, meta):

    # Define [HTML Title element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title) ```<title>```
    # from first markdown heading as ```pagetitle```
    # if it is missing in meta
    if 'pagetitle' not in meta:
        firsthead = re.search('(?m)^#+(.*)', proserial[0])
        if (firsthead != None):
            meta['pagetitle'] = firsthead.group(1).strip()

    return meta


def get_slugs (sourcefile, source_directory_realpath, config_namespaceseparator):

    ## create target file slugs
    lemma, file_extension   = os.path.splitext(os.path.basename(sourcefile) )
    ## make a source directory relative path
    contentdir              = os.path.dirname(sourcefile[len(source_directory_realpath) +1 :]) ## + 1 to remove leading slash
    # use source directories as __namespace__, with customizing namespaceseperators (```namespace:pagetitle```).
    slugdir                 = contentdir.replace(os.sep, config_namespaceseparator)

    ## slugs with directories need an trailings namespaceseparator
    if (len(contentdir ) > 0):
        slugdir =  slugdir + config_namespaceseparator

    slugs = {}
    slugs['lemma']   = lemma
    slugs['dirlimb'] = slugdir + lemma

    slugs['html']    = slugdir + lemma + '.html'
    slugs['json']    = slugdir + lemma + '.json'

    source_directory_realpath_len   =      len(source_directory_realpath)
    slugs['source']  = sourcefile[source_directory_realpath_len:]

    return slugs


def get_source_git_meta(sourcefile, config_source, source_git_meta_meta):

    try:
        repo = git.Repo(config_source, search_parent_directories=True)

        # https://git-scm.com/docs/pretty-formats
        source_git_meta = {}
        source_git_meta['last_name']     = repo.git.log('-1', '--format=' + source_git_meta_meta['last_name_format'], sourcefile)
        source_git_meta['last_email']    = repo.git.log('-1', '--format=' + source_git_meta_meta['last_email_format'], sourcefile)
        source_git_meta['last_date']     = repo.git.log('-1', '--format=' + source_git_meta_meta['last_date_format'], sourcefile)
        source_git_meta['last_subject']  = repo.git.log('-1', '--format=' + source_git_meta_meta['last_subject_format'],  sourcefile)

        # TODO oldest_*

        return source_git_meta

    except:
        return

