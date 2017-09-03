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
import time

import bs4

from g_sorcery.db_layout import BSON_FILE_SUFFIX
from g_sorcery.exceptions import DownloadingError
from g_sorcery.g_collections import Package, serializable_elist
from g_sorcery.package_db import DBGenerator, PackageDB
import subprocess


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

    def get_download_uries(self, common_config, config):
        """
        Get URI of packages index.
        """
        self.repo_uri = config["repo_uri"]
        return [{"uri": self.repo_uri + "nodepkg?%3Aaction=index", "output": "packages"}]

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

        # npm install all-the-package-names --save
        status, output = subprocess.getstatusoutput(
            "/home/sabayonuser/node_modules/.bin/all-the-package-names")
        if status == 0:
            data = self.parse_data(output)
        else:
            raise Exception('all-the-package-names error!')
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
            if i >= 10:
                break
            status, output = subprocess.getstatusoutput(
                "npm view " + entry + ' name description version repository license dist')
            if status == 0:
                import re
                import json
                output = re.sub(r'([a-zA-Z_]+) =', r'"\1":', output)
                output = re.sub(r' ([a-zA-Z_]+):', r' "\1":', output)
                output = re.sub("(['}])\n", r"\1,\n", output)
                output = '{' + output.replace("'", '"') + '}'
                print(output)

                pp = json.loads(output)
                print(pp)
            else:
                continue

            package, description, version = pp['name'], pp['description'], pp['version']
            print(package)
            data["index"][(package, version)] = (description, pp)

        return data

    def process_data(self, pkg_db, data, common_config, config):
        """
        Process parsed package data.
        """
        category = "dev-nodejs"
        pkg_db.add_category(category)

        common_data = {}
        common_data["eclasses"] = ['g-sorcery', 'gs-nodepkg']
        common_data["maintainer"] = [{'email': 'tastuteche@yahoo.com',
                                      'name': 'Tastu Teche'}]
        common_data["dependencies"] = serializable_elist(separator="\n\t")
        pkg_db.set_common_data(category, common_data)

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

            pkg_data = pp

            files_src_uri = pp["dist"]["tarball"]
            md5 = pp["dist"]["shasum"]

            homepage = pp["repository"]["url"]
            pkg_license = ''
            py_versions = []

            if "license" in pp:
                pkg_license = pp["license"]
            pkg_license = self.convert(
                [common_config, config], "licenses", pkg_license)

            filtered_package = "".join(
                [x for x in package if ord(x) in allowed_ords_pkg])
            description = "".join(
                [x for x in description if ord(x) in allowed_ords_desc])
            filtered_version = version
            match_object = re.match("(^[0-9]+[a-z]?$)|(^[0-9][0-9\.]+[0-9][a-z]?$)",
                                    filtered_version)
            if not match_object:
                filtered_version = pseudoversion

            ebuild_data = {}
            ebuild_data["realname"] = package
            ebuild_data["realversion"] = version

            ebuild_data["description"] = description
            ebuild_data["longdescription"] = description

            ebuild_data["homepage"] = homepage
            ebuild_data["license"] = pkg_license
            ebuild_data["source_uri"] = files_src_uri
            ebuild_data["md5"] = md5

            pkg_db.add_package(
                Package(category, filtered_package, filtered_version), ebuild_data)
