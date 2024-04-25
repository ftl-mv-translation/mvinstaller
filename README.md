# mvinstaller

Installer application for the localized versions of FTL: Multiverse.

![image](https://user-images.githubusercontent.com/11943013/189501931-0eff4fab-6cc3-47df-8347-6897a941b5d8.png)

### Localizing the app

Send PR that modifies the `locale/` directory.

### Dealing with new Hyperspace versions, (unlikely) FTL updates, or MV addons

See [`mvinstaller/signatures.py`](mvinstaller/signatures.py) to update those information.
The file serves as the database for the installer and it's self-explanatory.

Help wanted: If you're playing FTL on the Humble Bundle/Origin/Xbox/GOG then you may help adding support for those platforms.
Currently the app fully supports Steam installation, but the builds from other ESDs are only partially supported with different progress.
See [#15](https://github.com/ftl-mv-translation/mvinstaller/issues/15) for the instructions.

#### Adding/updating addons

1. Add your addon to the `FixedAddonsList` class in `signatures.py`.
   * Note that it's order-sensitive. Slipstream Mod Manager will install the addons in the order of listing.
   * Adjust the `locale` field to which language your addon supports.
     If it's language-agnostic then set it to `None` instead and it'll be available for every language.
2. Send PR

### Building the app

The app is a standard Python package. Use poetry or pip with virtualenv to install the project and invoke
`python mvinstaller`.
