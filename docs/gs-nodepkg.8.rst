=======
gs-nodepkg
=======

-----------------------------------
manage overlays for NPM repository
-----------------------------------

:Author: Written by Tastu Teche <tastuteche@yahoo.com>. GSoC idea
	 and mentorship by Rafael Martins. Lots of help and improvements
	 by Brian Dolbec.
:Date:   2015-04-22
:Copyright: Copyright (c) 2013-2015 Tastu Teche, License: GPL-2
:Version: 0.2.1
:Manual section: 8
:Manual group: g-sorcery


SYNOPSIS
========

**gs-nodepkg** **-o** *OVERLAY* [**-r** *REPO*] **sync**

**gs-nodepkg** **-o** *OVERLAY* [**-r** *REPO*] **list**

**gs-nodepkg** **-o** *OVERLAY* [**-r** *REPO*] **generate** *PACKAGE*

**gs-nodepkg** **-o** *OVERLAY* [**-r** *REPO*] **install** *PACKAGE*

**gs-nodepkg** **-o** *OVERLAY* [**-r** *REPO*] **generate-tree** [**-d**]

DESCRIPTION
===========

**gs-nodepkg** is an ebuild generator for NdoeJS npm repository.

There are two ways of using **gs-nodepkg**:

    * use it with **layman**

      In this case all you need to do is install **gs-nodepkg**.
      Then you should just run `layman -L` as
      root and find an overlay you want (**nodepkg**). Type of overlay will be
      displayed as *g-sorcery*. Then you add this overlay as
      usual. That's the recommended way of
      using **gs-nodepkg**. Be aware that by default **nodepkg** will
      contain lots of ebuilds, you'll need to change config before
      adding the overlay (see below) to prevent this.

    * use it as stand-alone tool (not recommended)

      In this case you should create an overlay (see **portage** documentation), sync it and populate
      it with one or more ebuilds. Then ebuilds could be installed by emerge or by **gs-nodepkg** tool.


OPTIONS
=======

**--overlay** *OVERLAY*, **-o** *OVERLAY*
    Overlay directory. This option is mandatory if there is no
    **default_overlay** entry in a backend config.

**--repository** *REPO*, **-r** *REPO*
    Repository name. This option is not mandatory. If present should be **ctan**.

COMMANDS
========

**sync**
    Synchronize a repository database.

**list**
    List packages available in a repository.

**generate**
    Generate a given ebuild and all its dependencies.

**install**
    Generate and install an ebuild using your package mangler.

**generate-tree**
    Generate entire overlay structure. Without option **-d** after
    this command sources are not fetched during generation and there
    are no entries for them in Manifest files.

FILES
=====
**/etc/g-sorcery/gs-nodepkg.json**
    Backend config.

**/etc/layman/overlays/gs-nodepkg-overlays.xml**
    List of available repositories.

EXAMPLES
========

Using gs-nodepkg with layman
    Execute

    **layman -L**

    If you see there a **nodepkg** overlay then everything should work.

    **IMPORTANT**

    Change *g-sorcery.cfg* so it includes a list of packages you need,
    otherwise **gs-nodepkg** will generate a huge amount of ebuilds (see
    *g-sorcery.cfg* man page):

    .. code-block::

       [main]
       package_manager=portage

       [gs-nodepkg]
       nodepkg_packages=npm-remote-ls

    Packages list is whitespace separated.
    To list available packages use list
    command from the next section.

    Add overlay as usual:

    **layman -a nodepkg**

    Emerge any package from it using **emerge**.

Generating user ebuilds in user overlay (not recommended)
    Create new user overlay. Run

    **gs-nodepkg -o** *OVERLAY_DIRECTORY* **-r ctan** **sync**

    List packages:

    **gs-nodepkg -o** *OVERLAY_DIRECTORY* **-r ctan** **list**

    Install any package you want:

    **gs-nodepkg -o** *OVERLAY_DIRECTORY* **-r ctan** **install** *PACKAGE*

    Note, that if you call **generate-tree** command your overlay
    will be wiped and overlay tree for a given repository will be generated. Be careful!

NOTES
=====

1. At the moment the only package mangler **gs-nodepkg** supports is **portage**.

SEE ALSO
========

**gs-elpa**\(8), **g-sorcery.cfg**\(8), **portage**\(5), **emerge**\(1), **layman**\(8)
