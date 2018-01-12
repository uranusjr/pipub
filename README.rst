=====
PiPuB
=====

PiPuB (read as a word, pih-pub) is a build tool that exports package
requirements from the project's ``Pipfile`` and ``pyproject.toml`` to produce
a ``setup.cfg`` that you can use to distribute the package to PyPI.

A work in progress.


How to
======

You can read this project's ``pyproject.toml`` and ``setup.py`` as an example.


Package Information from ``pyproject.toml`` and ``Pipfile``
-----------------------------------------------------------

Create a ``pyproject.toml`` to contain most of your package's metadata. All
values should go under the ``tool.pipub`` table.

Everything available in the ``setup.cfg`` is available [#]_ (but you might want to
skip a few; see below), and you can ultilise the TOML syntax:

    * You can use TOML constructs (booleans, numbers, lists, and tables). PiPuB
      does the write thing automatically.
    * ``file:`` and ``attr:`` directives can be written as an inline table.

(Many obscure edge cases are currently not supported. Patches welcomed.)

.. [#] See the `Configuring setup() using setup.cfg files`_ section in the
       Building and Distributing Packages with Setuptools documentation.

.. _`Configuring setup() using setup.cfg files`: http://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files

Two entries will be extracted from ``Pipfile`` if they do not present in
``pyproject.toml``:

    * ``options.install_requires`` will be populated from ``packages``.
    * ``options.python_requires`` will be populated from
      ``requires.python_version``.

IMPORTANY: they will be populated from ``Pipfile`` *only if they don't already
have an entry in ``pyproject.toml``*.

Since population from ``setup.cfg`` only exists in Setuptools >= 30.3.0, you
should add a ``[build-system]`` section in ``pyproject.toml`` as well::

    [build-system]
    requires = ["setuptools>=30.3.0", "wheel"]


See `PEP 518`_ for more information.

.. _`PEP 518`: https://www.python.org/dev/peps/pep-0518/


``setup.py``
------------

Create a ``setup.py``. It does not need to contain much information, only
those you want to calculate dynamically::

    from setuptools import setup

    __version__ = ... # Read the version dynamically from a file or something.
    setup(version=__version__)


When Releasing
--------------

Be sure to read the `official packaging tutorial`_. PiPuB only process
``setup.cfg`` (and as an extention the ``setup()`` call in ``setup.py``); you
still need to provide other required files.

.. _`official packaging tutorial`: https://packaging.python.org/tutorials/distributing-packages/

PiPuB provides a few subcommands to help you publish a package. A typical
release process would look like this::

    # Generate setup.cfg
    pipub prepare

    # Call `python setup.py` with given arguments.
    pipub build sdist bdist_wheel

    # Call `python -m twine upload` with given arguments.
    pipub upload dist/*


Special Considerations
======================

Since ``setup.cfg`` is generated dynamically, I recommend putting it in your
VCS's ignore list (e.g. ``.gitignore``) so it doesn't drift out of sync.

A downside to this approach is that users can no longer download and install
your package directly from source (e.g. a Zip download from GitHub) without
reconstructing ``setup.cfg`` themselves. There's not much can be done here.
You can instruct them what to do in documentation, or commit a pre-generated
``setup.cfg`` in so they can use it (and carefully keep it synced). Or maybe
you just don't care. I know I don't.
