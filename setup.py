#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    setup.py
    ~~~~~~~~

    installation script

    :copyright: (c) 2013-2015 by Tastu Teche
    :license: GPL-2, see LICENSE for more details.
"""

from distutils.core import setup

setup(name='gs-nodepkg',
      version='0.2.1',
      description='g-sorcery backend for nodepkg packages',
      author='Tastu Teche',
      author_email='tastuteche@yahoo.com',
      packages=['gs_nodepkg'],
      package_data={'gs_nodepkg': ['data/*']},
      scripts=['bin/gs-nodepkg-generate-db', 'bin/gs-nodepkg'],
      data_files=[('@GENTOO_PORTAGE_EPREFIX@/etc/g-sorcery/', ['gs-nodepkg.json']),
                  ('@GENTOO_PORTAGE_EPREFIX@/etc/layman/overlays/', ['gs-nodepkg-overlays.xml'])],
      license='GPL-2',
      )
