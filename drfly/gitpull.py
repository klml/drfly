#!/usr/bin/env python
# coding: utf-8

# git pull and trigger render for new and changed files
import git
import os
import sys

import path_router


def gitpull(sourcedirectory):

    try:
        repo = git.Repo(sourcedirectory , search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError:
        # TODO really double check with webhook
        print('no git repo')
        return ['no git repo']

    ## register current commit, before git pull,
    oldcommmit = repo.head.commit.tree
    repo_remotes_origin_pull = repo.remotes.origin.pull()

    ## get new and changed files since commit before
    updated_files = repo.git.diff('--name-only', 'HEAD', oldcommmit).split()

    result = []
    # cant do this with a webservice,
    # gitpull should also work without webhook.py depending http://webpy.org/
    for updated_file in updated_files:
        parse_result = path_router.build_single(updated_file ,  sourcedirectory)
        result.extend(parse_result)
    return result

if __name__ == "__main__":
    print(gitpull(sys.argv[1:][0]))

