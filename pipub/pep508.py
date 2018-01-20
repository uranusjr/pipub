"""Implement logic to dump a requirement specification to PEP-508 format.

https://www.python.org/dev/peps/pep-0508/
"""

import collections
import warnings


class DependencyNotSupported(ValueError):
    pass


class EditableNotSupported(DependencyNotSupported):
    pass


class LocalNotSupported(DependencyNotSupported):
    pass


class SilentDropWarning(UserWarning):
    pass


def dump_requirement(key, value):
    # Special formats.
    if isinstance(value, str):
        value = {'version': value}
    elif not isinstance(value, collections.abc.Mapping):
        raise TypeError('must be str or mapping, not {!r}'.format(type(value)))

    link = None     # Dependency link for this requirement, if needed.
    dependency = [key]

    if value.pop('editable', None):
        raise EditableNotSupported()
    if 'path' in value:
        raise LocalNotSupported()

    if value.get('extras'):
        dependency.append('[{}]'.format(','.join(value.pop('extras'))))

    version = value.pop('version', '*')
    if version != '*':
        dependency.append(version)

    if value.get('file'):
        # TODO: Support @version, #fragment, etc.
        link = value.pop('file')
    # TODO: Support VCS link parsing.

    dependency = ''.join(dependency)

    if link:
        dependency = '{} @ {}'.format(dependency, link)
    if value.get('markers'):
        dependency = '{} ; {}'.format(dependency, value.pop('markers', None))

    if value:   # Stray keys.
        warnings.warn(' '.join(value.keys()), SilentDropWarning)

    return dependency
