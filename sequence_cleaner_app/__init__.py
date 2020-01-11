# -*- coding: utf-8 -*-

import pkg_resources

try:
    version = pkg_resources.require("sequence_cleaner")[0].version
except:
    raise ValueError('Cannot find version number')
