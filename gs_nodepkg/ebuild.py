#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    ebuild.py
    ~~~~~~~~~
    
    ebuild generation
    
    :copyright: (c) 2013 by Tastu Teche
    :license: GPL-2, see LICENSE for more details.
"""

import collections
import os

from g_sorcery.ebuild import DefaultEbuildGenerator

Layout = collections.namedtuple("Layout",
    ["vars_before_inherit", "inherit", "vars_after_description", "vars_after_keywords"])
  

class NodepkgEbuildWithoutDigestGenerator(DefaultEbuildGenerator):
    """
    Implementation of ebuild generator without sources digesting.
    """
    def __init__(self, package_db):

        vars_before_inherit = \
          ["realname", "realversion",
           {"name" : "repo_uri", "value" : 'https://www.npmjs.com/package/${REALNAME}/'},
           {"name" : "sourcefile", "value" : '${REALNAME}-${REALVERSION}.tgz'}, {"name" : "nodejs_compat", "raw" : True}]

        inherit = ["gs-nodepkg"]
        
        vars_after_description = \
          ["homepage", "license"]

        vars_after_keywords = \
          []

        layout = Layout(vars_before_inherit, inherit, vars_after_description, vars_after_keywords)

        super(NodepkgEbuildWithoutDigestGenerator, self).__init__(package_db, layout)

class NodepkgEbuildWithDigestGenerator(DefaultEbuildGenerator):
    """
    Implementation of ebuild generator with sources digesting.
    """
    def __init__(self, package_db):

        vars_before_inherit = \
          ["realname", "realversion",
           {"name" : "digest_sources", "value" : "yes"}, {"name" : "nodejs_compat", "raw" : True}]

        inherit = ["gs-nodepkg"]
        
        vars_after_description = \
          ["homepage", "license",
           {"name" : "src_uri", "value" : '"http://registry.npmjs.org/${REALNAME}/-/${REALNAME}-${REALVERSION}.tgz"'}]

        vars_after_keywords = \
          []

        layout = Layout(vars_before_inherit, inherit, vars_after_description, vars_after_keywords)

        super(NodepkgEbuildWithDigestGenerator, self).__init__(package_db, layout)
