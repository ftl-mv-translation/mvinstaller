# mvinstaller

Installer application for the localized versions of FTL: Multiverse.

### Localizing the app

Send PR that modifies the `locale/` directory.

### Dealing with new Hyperspace versions, (unlikely) FTL updates, adding/updating new MV addons

See [`mvinstaller/signatures.py`](mvinstaller/signatures.py) to update those information.
The file is self-explanatory.

Help wanted: If you're playing FTL on the Origin/Xbox/GOG then you might help adding support for those platforms.
Currently the app supports Steam installation only.

### Building the app

The app is a standard Python package. Use pip (w/ virtualenv or poetry) to install the project
and invoke `python mvinstaller`.
