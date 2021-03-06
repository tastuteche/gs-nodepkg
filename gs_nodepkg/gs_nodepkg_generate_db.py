#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    nodepkg_db.py
    ~~~~~~~~~~

    nodepkg database generation

    :copyright: (c) 2013-2015 by Tastu Teche
    :license: GPL-2, see LICENSE for more details.
"""

import argparse
import os
import sys

from g_sorcery.compatibility import TemporaryDirectory
from g_sorcery.exceptions import FileJSONError
from g_sorcery.fileutils import copy_all, FileJSON
from g_sorcery.logger import Logger

from .nodepkg_db import NodepkgDBGenerator

def main():
    import portage
    eprefix = portage.data._target_eprefix()
    
    parser = argparse.ArgumentParser(description='Package DB generator for gs-nodepkg.')
    parser.add_argument('db_dirname', help='directory to store DB')
    parser.add_argument('-c', '--count', help='count of records that should be processed',
                        default=None)
    parser.add_argument('--layout-version', help='DB layout version', default='1')
    parser.add_argument('--structure-version', help='DB structure version', default='1')
    parser.add_argument('-f', '--fmt', help='packages file format (json or bson)', default='bson')

    args = parser.parse_args(sys.argv[1:])

    db_name = args.db_dirname
    count = args.count
    layout_version = int(args.layout_version)
    structure_version = int(args.structure_version)
    fmt = args.fmt
    if count:
        count = int(count)

    logger = Logger()
    cfg_path = None
    for path in '.', '~', eprefix + '/etc/g-sorcery':
        current = os.path.join(path, "gs-nodepkg.json")
        if (os.path.isfile(current)):
            cfg_path = path
            break
    if not cfg_path:
        logger.error('no config file for gs-nodepkg backend\n')
        return -1
    cfg_f = FileJSON(cfg_path, "gs-nodepkg.json", ['package'])
    try:
        config = cfg_f.read()
    except FileJSONError as e:
        logger.error('error loading config file for gs-nodepkg: ' + str(e) + '\n')
        return -1

    generator = NodepkgDBGenerator(preferred_layout_version=layout_version,
                                preferred_db_version=structure_version,
                                preferred_category_format=fmt,
                                count=count)
    temp_dir = TemporaryDirectory()
    pkg_db = generator(temp_dir.name, "nodepkg",
                       config=config["repositories"]["nodepkg"],
                       common_config=config["common_config"])
    if os.path.exists(db_name):
        os.system('rm -rf ' + db_name + '/*')
    else:
        os.mkdir(db_name)
    copy_all(os.path.join(temp_dir.name, "nodepkg/db"), db_name)
    os.system('tar cvzf ' +  db_name + '.tar.gz ' + db_name)

if __name__ == "__main__":
    sys.exit(main())
