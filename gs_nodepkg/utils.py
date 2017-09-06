import json
import subprocess
import re
from g_sorcery.g_collections import serializable_elist
from g_sorcery.g_collections import Dependency


def get_pkg_json(entry):
    status, output = subprocess.getstatusoutput(
        "npm view " + entry + ' name description version repository license dist dependencies devDependencies')
    if status == 0:
        output = output.replace('"', '___')
        output = re.sub(r'([-a-zA-Z_0-9]+) = ' +
                        r"(['{\[]| \n)", r'"\1": ' + r'\2', output)
        output = re.sub(r' ([-a-zA-Z_0-9]+): ' +
                        r"([']|false,|[0-9]+,)", r' "\1": ' + r'\2', output)
        output = re.sub("(['}\]])\n", r"\1,\n", output)
        output = '{' + \
            output.replace("'", '"') + '}'

        pp = json.loads(output)
    else:
        pp = None
    return (status, pp, output)


def convert(configs, dict_name, value):
    """
    Convert a value using configs.
    This function is aimed to be used for conversion
    of values such as license or package names.

    Args:
        configs: List of configs.
        dict_name: Name of a dictionary in config
    that should be used for conversion.
        value: Value to convert.

    Returns:
        Converted value.
    """
    result = value
    for config in configs:
        if config:
            if dict_name in config:
                transform = config[dict_name]
                if value in transform:
                    result = transform[value]
    return result


def get_ebuild_data(pp, common_config={}, config={}):
    ebuild_data = {}
    package, version = pp['name'], pp['version']
    if 'description' in pp:
        description = pp['description']
    else:
        description = ''
    ebuild_data["realname"] = package
    ebuild_data["realversion"] = version

    ebuild_data["description"] = description
    ebuild_data["longdescription"] = description

    ebuild_data["homepage"] = pp["repository"]["url"]
    pkg_license = ''
    if "license" in pp:
        pkg_license = pp["license"]
        pkg_license = convert(
            [common_config, config], "licenses", pkg_license)

    ebuild_data["license"] = pkg_license
    ebuild_data["source_uri"] = pp["dist"]["tarball"]
    ebuild_data["md5"] = pp["dist"]["shasum"]
    if 'dependencies' in pp:
        ll = serializable_elist(separator="\n\t")
        for dep in pp["dependencies"].items():
            # print(dep)
            ll.append(Dependency('dev-nodejs', dep[0]))
        #print(ll, '@@@@@')
        ebuild_data["dependencies"] = ll
    else:
        ebuild_data["dependencies"] = ''
    if 'devDependencies' in pp:
        ebuild_data["devDependencies"] = pp["devDependencies"]
    else:
        ebuild_data["devDependencies"] = ''

    return ebuild_data


def get_common_data():
    common_data = {}
    common_data["eclasses"] = ['g-sorcery', 'gs-nodepkg']
    common_data["maintainer"] = [{'email': 'tastuteche@yahoo.com',
                                  'name': 'Tastu Teche'}]
    #common_data["dependencies"] = serializable_elist(separator="\n\t")
    return common_data
