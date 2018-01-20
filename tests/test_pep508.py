from pipub.pep508 import dump_requirement


# TODO: PEP 508 contains some test data that can be used to populate these.
# The problem is I don't know very well how they are represented in Pipfile.
# https://www.python.org/dev/peps/pep-0508/#complete-grammar


def test_star():
    assert dump_requirement('mosql', '*') == 'mosql'


def test_pinned():
    assert dump_requirement('mosql', '<0.7') == 'mosql<0.7'


def test_extras():
    dumped = dump_requirement('requests', {'extras': ['socks', 'security']})
    assert dumped == 'requests[socks,security]'


def test_markers():
    dumped = dump_requirement('unittest2', {
        'version': ">=1.0,<3.0",
        'markers': "python_version < '2.7.9'",
    })
    assert dumped == "unittest2>=1.0,<3.0 ; python_version < '2.7.9'"


def test_file():
    dumped = dump_requirement('oauth2', {
        'file': 'https://github.com/tseaver/python-oauth2/archive/py3.zip',
    })
    expected = (
        'oauth2 @ '
        'https://github.com/tseaver/python-oauth2/archive/py3.zip'
    )
    assert dumped == expected
