__all__ = []


def get_version():
    from pathlib import Path
    return Path(__file__).with_name('version.txt').read_text().strip()


__version__ = get_version()
