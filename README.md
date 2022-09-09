# mvinstaller

Installer application for the localized versions of FTL: Multiverse.

### Localizing the app

Send PR that modifies the `locale/` directory.

### Dealing with new Hyperspace versions, (unlikely) FTL updates, or MV addons

See [`mvinstaller/signatures.py`](mvinstaller/signatures.py) to update those information.
The file serves as a self-explanatory database for the installer.

Help wanted: If you're playing FTL on the Origin/Xbox/GOG then you may help adding support for those platforms.
Currently the app supports Steam installation only.
See [#15](https://github.com/ftl-mv-translation/mvinstaller/issues/15) for the instructions.

#### Adding/updating a new addon

1. Copy your addon's `metadata.xml` to the `addon_metadata` directory.
   Rename the file to have a slug that fits your addon's name.
2. Add your addon to the `AddonsList` class.
   * Note that it's order-sensitive. Slipstream Mod Manager will install the addons in the order of listing.
   * Adjust the `metadata_name` field to which `metadata.xml` has been renamed in step 1.
   * Adjust the `locale` field to which language your addon supports.
     If it's language-agnostic then set it to `None` instead and it'll be available for every language.

### Building the app

The app is a standard Python package. Use poetry or pip with virtualenv to install the project and invoke
`python mvinstaller`.

