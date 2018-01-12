import collections.abc
import configparser
import contextlib
import numbers
import pathlib
import warnings

import pipfile
import toml


def convert(value):
    """Convert a TOML value to INI.
    """
    if isinstance(value, str):
        return value
    if isinstance(value, numbers.Number):
        return str(value).lower()
    if isinstance(value, collections.abc.Sequence):
        s = '\n'.join(convert(v) for v in value)
        if len(value) > 1:
            return '\n' + s
        return s
    if isinstance(value, collections.abc.Mapping):
        s = '\n'.join(f'{key}: {convert(val)}' for key, val in value.items())
        if len(value) > 1:
            return '\n' + s
        return s
    raise ValueError(f'can not handle {type(value)} instance')


def read_pyproject(parser, path):
    with path.open() as f:
        try:
            data = toml.load(f)['tool']['pipub']['setup']
        except KeyError as e:
            warnings.warn(f'no section {e} in pyproject.toml')
            data = {}
    for name, group in data.items():
        if not parser.has_section(name):
            parser.add_section(name)
        for key, value in group.items():
            parser[name][key] = convert(value)


def iter_requirements(packages):
    for name, pin in packages.items():
        if pin == '*':
            yield name
        else:   # TODO: Actually support pin markers.
            yield f'{name}{pin}'


def add_pipfile_entry(parser, section, key, value):
    if not parser.has_section(section):
        parser.add_section(section)
    if key in parser[section] and parser[section][key] != value:
        warnings.warn(f'[{section}].{key} exists, not overwriting')
    parser[section][key] = value


def read_pipfile(parser, path):
    with path.open() as f:
        data = toml.load(f)
    add_pipfile_entry(
        parser, 'options', 'install_requires',
        convert(list(iter_requirements(data.get('packages', {})))),
    )
    add_pipfile_entry(
        parser, 'options.extras_require', 'dev',
        convert(list(iter_requirements(data.get('dev-packages', {})))),
    )
    with contextlib.suppress(KeyError):
        python_version = convert(data['requires']['python_version'])
        add_pipfile_entry(parser, 'options', 'python_requires', python_version)


class Project:

    def __init__(self, *, root):
        self.root = root

    @classmethod
    def autodiscover(cls):
        root = pathlib.Path(pipfile.Pipfile.find()).parent.resolve(strict=True)
        return cls(root=root)

    def as_cfg(self):
        parser = configparser.ConfigParser()
        try:
            read_pyproject(parser, self.root.joinpath('pyproject.toml'))
        except FileNotFoundError:
            warnings.warn(f'pyproject.toml not found')
        try:
            read_pipfile(parser, self.root.joinpath('Pipfile'))
        except FileNotFoundError:
            warnings.warn('Pipfile not found')
        return parser

    def write_cfg(self, path):
        parser = self.as_cfg()
        with path.open('w') as f:
            parser.write(f, space_around_delimiters=True)
