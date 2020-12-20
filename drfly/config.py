#!/usr/bin/env python
# coding: utf-8

import os
import yaml

def config( source_directory ):

    module_path = os.path.abspath(os.path.dirname(__file__))
    config_global = os.path.join( module_path , "meta.global.yaml")
    config_local  = source_directory + os.sep + 'meta.yaml'

    config        = yaml.safe_load( open( config_global ) )
    if ( os.path.isfile( config_local ) ):
        config.update(    yaml.safe_load( open( config_local  ) ) )

    return config

