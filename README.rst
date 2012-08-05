=======
UFO2OTF
=======

Ufo2otf is a command line utility that takes UFO font sources and generates
OTF’s and webfonts.

Summary
-------
::

    usage: ufo2otf [-h] [--webfonts] [--afdko] infiles [infiles ...]

    positional arguments:
      infiles     The source UFO files

    optional arguments:
      -h, --help  show this help message and exit
      --webfonts  Generate webfonts in a ./webfonts subfolder
      --afdko     Generate the OTF with Adobe Font Development Kit for Opentype


Usage examples
--------------
::

    $ ufo2otf OpenBodoni.ufo

will create a file called OpenBodoni.otf.
::

    $ ufo2otf OpenBodoni-Regular.ufo OpenBodoni-Italic.ufo OpenBodoni-Bold.ufo

will create OpenBodoni-Regalur.otf, OpenBodoni-Italic.otf and OpenBodoni-Bold.otf.


Fontforge
---------

By default, ufo2otf uses FontForge to generate the otf files. FontForge is a
free and open source font editor that comes with a python extension. The
python extension has access to the functionality of FontForge without needing
to launch the graphical program itself.

Ufo2otf will warn you if FontForge is not present. Installing it can be as
easy as:

debian, ubuntu::

    $ sudo apt-get install fontforge python-fontforge

os x::

    $ brew install fontforge

More info see:
http://openfontlibrary.org/wiki/How_to_install_FontForge

AFDKO
-----

Ufo2otf can also use the AFDKO to generate the fontfiles.

The Adobe Font Development Kit for Opentype are a set of tools made available
by Adobe that can help you generate Opentype/CFF fonts from PostScript
sources, and to add OpenType features in the progress.

Since the AFDKO is not open source, and not installable on Linux, it doesn’t
make a lot of sense for Open Source projects. But it can be useful to have
around, if only to compare the output to that of FontForge.

Please check http://www.adobe.com/devnet/opentype/afdko.html for installation
instructions. Subsequently, one needs to install Tal Leming’s ufo2afdko
package which in turn depends on Robofab:

http://code.typesupply.com/wiki/ufo2fdk
http://robofab.org/

Webfonts
--------

Passing the option ``--webfonts`` will generate a subfolder called webfonts. Ufo2otf
autohints the font and proceeds to generate ttf and woff files. Feature
releases will add support for eot, and automatically generating an appropriate
CSS stylesheet.

When using the AFDKO to convert the fonts the webfonts option is not
available.

UFO
---

UFO is an open and exchangable format for fonts.It is easy to write programs
that process UFO fonts, and they play well with versioning systems like Git.

http://unifiedfontobject.org/

History
-------

Ufo2otf has been developed by Eric Schrijver for the Open Baskerville font
project, a collaborative open source typeface.

http://klepas.org/openbaskerville/

License
-------

Ufo2otf is licensed under the BSD license (see LICENSE.txt).

Argparse
--------

This software includes a version of Python 2.7’s argparse module that is
compatible with earlier version of Python. The author is Steven Bethard and
the license is the Python Software Foundation license
http://docs.python.org/license.html
