#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    backend.py
    ~~~~~~~~~~
    
    nodepkg backend
    
    :copyright: (c) 2013 by Tastu Teche
    :license: GPL-2, see LICENSE for more details.
"""

import os

from g_sorcery.backend import Backend
from g_sorcery.metadata import MetadataGenerator
from g_sorcery.eclass import EclassGenerator
from g_sorcery.fileutils import get_pkgpath

from .nodepkg_db import NodepkgDBGenerator
from .ebuild import NodepkgEbuildWithoutDigestGenerator, NodepkgEbuildWithDigestGenerator


class NodepkgEclassGenerator(EclassGenerator):
    """
    Implementation of eclass generator. Only specifies a data directory.
    """

    def __init__(self):
        super(NodepkgEclassGenerator, self).__init__(
            os.path.join(get_pkgpath(__file__), 'data'))


instance = Backend(NodepkgDBGenerator,
                   NodepkgEbuildWithDigestGenerator, NodepkgEbuildWithoutDigestGenerator,
                   NodepkgEclassGenerator, MetadataGenerator, sync_db=False)
