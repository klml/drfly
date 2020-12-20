#!/usr/bin/env python
# coding: utf-8

import codecs

## PROSErial
# for rendering (template, menue etc) or html metatags are at the __bottom__ of the page and only __optional__ 
# [PROSErial](https://github.com/klml/PROSErial))

def splitproseserial( sourcefile, metaseparator ):
    ## try if file is text (like md, css, js, yaml) and not a binary (jpg, gif)
    try:
        with codecs.open( sourcefile , 'r', encoding="utf-8") as opensourcefile:
            source = opensourcefile.read()
        return source.split( metaseparator )   

    except UnicodeDecodeError:
        return False

