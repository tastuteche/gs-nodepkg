This is [g-sorcery](https://github.com/jauhien/g-sorcery) backend for NdoeJS NPM packages.


# Installation

```
emerge -va gs-nodepkg
```

This will install all the necessary dependencies, including g-sorcery with BSON support,
layman with g-sorcery support and pymongo (used for BSON manipulation).

# Usage

There are two ways of using **gs-nodepkg**

## Using gs-nodepkg with [layman](https://wiki.gentoo.org/wiki/Layman)

It the the recommend way and I strongly suggest it.

Then you should just run `layman -L` as
root and find an overlay you want. Type of overlay will be
displayed as *g-sorcery*. Then you add this overlay as
usually and emerge packages you want. It's all you need to do. Example:

```
layman -L
layman -a nodepkg
emerge -va npm-remote-ls
```

There is 1 gs-nodepkg overlay currently: [nodepkg](https://www.npmjs.com).

When using **gs-nodepkg** with layman you can populate overlay only with packages you want.
To do so you should add a section named gs-nodepkg to */etc/g-sorcery/g-sorcery.cfg*.
In this section you can add entries named REPO_packages (REPO here is the name
of repository you want to add -- nodepkg) which are space separated lists of packages you need.
Note, that at the moment **gs-nodepkg** doesn't support dependencies for nodepkg packages, so you need to add
to this list package itself and all its dependencies.

```
[main]
package_manager=portage

[gs-nodepkg]
nodepkg_packages=npm-remote-ls
```
I strongly recommend to do so, as nodepkg overlay is quite big and you may be
do not want generate all the ebuilds from it. To list available packages use
the list command from the next section giving it appropriate layman overlay directory as argument.


## Using gs-nodepkg as stand-alone tool (strongly not recommended)

In this case you should create an overlay (see **portage** documentation), sync it and populate
it with one or more ebuilds. Then ebuilds could be installed by emerge or by **gs-nodepkg** tool.
This is not the recommended way and may be removed in the future.

Create new user overlay:

```
gs-nodepkg -o $OVERLAY_DIRECTORY -r nodepkg sync
```

List packages:

```
gs-nodepkg -o $OVERLAY_DIRECTORY -r nodepkg list
```

Install any package you want:

```
gs-nodepkg -o $OVERLAY_DIRECTORY -r nodepkg install $PACKAGE
```

Note, that if you call **generate-tree** command your overlay
will be wiped and overlay tree for a given repository will be generated. Be careful!

See man page of **gs-nodepkg** for further information.
