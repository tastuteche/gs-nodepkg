#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    nodepkg_db.py
    ~~~~~~~~~~

    nodepkg package database

    :copyright: (c) 2013-2015 by Tastu Teche
    :license: GPL-2, see LICENSE for more details.
"""

import datetime
import re
import os
from g_sorcery.db_layout import BSON_FILE_SUFFIX
from g_sorcery.g_collections import Package
from g_sorcery.package_db import DBGenerator, PackageDB
from .utils import get_ebuild_data, get_pkg_json, get_common_data
import subprocess


class NodepkgDB(PackageDB):
    def __init__(self, directory,
                 persistent_datadir=None,
                 preferred_layout_version=1,
                 preferred_db_version=1,
                 preferred_category_format=BSON_FILE_SUFFIX):
        super(PackageDB, self).__init__(directory=directory,
                                        persistent_datadir=persistent_datadir,
                                        preferred_layout_version=preferred_layout_version,
                                        preferred_db_version=preferred_db_version,
                                        preferred_category_format=preferred_category_format)

    def get_package_description(self, package):
        """
        Get package ebuild data.

        Args:
            package: g_collections.Package instance.

        Returns:
            Dictionary with package ebuild data.
        """
        # a possible exception should be catched in the caller
        pp = get_pkg_json(package.name)
        desc = dict(get_ebuild_data(pp))

        desc.update(get_common_data())
        return desc


class NodepkgDBGenerator(DBGenerator):
    """
    Implementation of database generator for nodepkg backend.
    """

    def __init__(self, package_db_class=PackageDB,
                 preferred_layout_version=1,
                 preferred_db_version=1,
                 preferred_category_format=BSON_FILE_SUFFIX,
                 count=None):
        super(NodepkgDBGenerator, self).__init__(package_db_class=package_db_class,
                                                 preferred_layout_version=preferred_layout_version,
                                                 preferred_db_version=preferred_db_version,
                                                 preferred_category_format=preferred_category_format)
        self.count = count
        self.gs_nodepkg_dir = self.get_gs_nodepkg_dir()
        self.pkg_cache_file = self.get_pkg_cache_file()

    def get_download_uries(self, common_config, config):
        """
        Get URI of packages index.
        """
        self.repo_uri = config["repo_uri"]
        return [{"uri": self.repo_uri + "nodepkg?%3Aaction=index", "output": "packages"}]

    def get_gs_nodepkg_dir(self):
        """
        Return location we store config files and data
        """
        return os.path.abspath("%s/.gs_nodepkg" % os.path.expanduser("~"))

    def get_pkg_cache_file(self):
        """
        Returns filename of pkg cache
        """
        return os.path.abspath('%s/pkg_list.pkl' % self.gs_nodepkg_dir)

    def download_data(self, common_config, config):
        """
        Obtain data for database generation.

        Args:
            common_config: Backend config.
            config: Repository config.

        Returns:
            Downloaded data.
        """
        uries = self.get_download_uries(common_config, config)
        uries = self.decode_download_uries(uries)
        data = {}

        def get_data():
            # npm install all-the-package-names --save
            # npm install npm-remote-ls --save
            status, output = subprocess.getstatusoutput(
                "%s/node_modules/.bin/all-the-package-names" % os.path.expanduser("~"))
            if status == 0:
                return output
            else:
                raise Exception('all-the-package-names error!')

        def get_data_from_cache():
            with open(self.pkg_cache_file, 'r') as f:
                return f.read()

        if not os.path.exists(self.gs_nodepkg_dir):
            os.mkdir(self.gs_nodepkg_dir)
        if os.path.exists(self.pkg_cache_file):
            output = get_data_from_cache()
        else:
            output = get_data()
            with open(self.pkg_cache_file, 'w') as f:
                f.write(output)

        data = self.parse_data(output)
        return data

    def parse_data(self, data_f):
        """
        Download and parse packages index. Then download and parse pages for all packages.
        """

        data = {}
        data["index"] = {}

        pkg_uries = []

        last = -1
        if self.count:
            last = self.count
        for i, entry in enumerate(data_f.split('\n')):
            # if i < 11750:
            if i > 10:
                continue
                # break
                pass
            (status, pp, output) = get_pkg_json(entry)
            if status == 0:
                print(i, '=========================')
                print(output)
                print('--------------------------')

                print(pp)
            else:
                continue

            package, version = pp['name'], pp['version']
            if 'description' in pp:
                description = pp['description']
            else:
                description = ''
            print(package)
            data["index"][(package, version)] = (description, pp)

        return data

    def process_data(self, pkg_db, data, common_config, config):
        """
        Process parsed package data.
        """
        category = "dev-nodejs"
        pkg_db.add_category(category)

        pkg_db.set_common_data(category, get_common_data())

        # todo: write filter functions
        allowed_ords_pkg = set(range(ord('a'), ord('z') + 1)) | set(range(ord('A'), ord('Z') + 1)) | \
            set(range(ord('0'), ord('9') + 1)) | set(list(map(ord,
                                                              ['+', '_', '-'])))

        allowed_ords_desc = set(range(ord('a'), ord('z') + 1)) | set(range(ord('A'), ord('Z') + 1)) | \
            set(range(ord('0'), ord('9') + 1)) | set(list(map(ord,
                                                              ['+', '_', '-', ' ', '.', '(', ')', '[', ']', '{', '}', ','])))

        now = datetime.datetime.now()
        pseudoversion = "%04d%02d%02d" % (now.year, now.month, now.day)

        for (package, version), (description, pp) in data["index"].items():

            filtered_package = "".join(
                [x for x in package if ord(x) in allowed_ords_pkg])
            description = "".join(
                [x for x in description if ord(x) in allowed_ords_desc])
            filtered_version = version
            match_object = re.match("(^[0-9]+[a-z]?$)|(^[0-9][0-9\.]+[0-9][a-z]?$)",
                                    filtered_version)
            if not match_object:
                filtered_version = pseudoversion

            ebuild_data = get_ebuild_data(pp, common_config, config)
            pkg_db.add_package(
                Package(category, filtered_package, filtered_version), ebuild_data)
