import os

def get_version():
    """Returns package version number"""
    # use auto-generated version file managed by setuptool_scm
    def use_version_file():
        try:
            from _version import __version__

            return __version__
        except ImportError:
            return False

    # use setuptool_scm library
    def use_setuptool_scm():
        try:
            from setuptools_scm import get_version

            return get_version(
                version_scheme="no-guess-dev", local_scheme="no-local-version"
            )
        except ImportError:
            return False

    # try reading package metadata using importlib
    def use_package_metadata():
        try:
            from importlib.metadata import version, PackageNotFoundError

            return version("fontnamer")
        except PackageNotFoundError:
            return False

    return (
        use_version_file() or use_setuptool_scm() or use_package_metadata() or "unknown"
    )



def file_exists(filepath):
    """Tests for existence of a file on the string filepath"""
    return os.path.exists(filepath) and os.path.isfile(filepath)

