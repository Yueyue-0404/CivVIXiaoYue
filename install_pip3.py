#!/usr/bin/env python
import os
import sys
from urllib.request import urlretrieve

PYPI_SIMPLE_URL = 'https://pypi.python.org/simple/'
PYPI_JSON_URL = 'https://pypi.python.org/pypi/{package}/json'

PYTHON_VERSION = '{}.{}'.format(*sys.version_info[:2])

def main():
    package = 'pip'
    try:
        from pip._internal.main import main as pipmain
    except ImportError:
        print("Installing %s..." % package)
        install(package)
    else:
        print("%s is already installed." % package)

def install(package):
    """Install the given package using pip."""
    if PYTHON_VERSION == "3.4":
        # For Python 3.4 we use the get-pip.py script
        url = 'https://bootstrap.pypa.io/get-pip.py'
        filename = 'get-pip.py'
        download(url, filename)
        run([sys.executable, filename])
    else:
        # For Python 2.7 and newer Python versions (&gt;=3.5)
        run([sys.executable, '-m', 'ensurepip', '--upgrade'])

def download(url, filename):
    """Download the given URL to the given filename."""
    print("Downloading %s to %s" % (url, filename))
    urlretrieve(url, filename)

def run(args):
    """Run the given command."""
    print("Running:", ' '.join(args))
    if os.name == 'nt':
        # On Windows, we need to explicitly specify the path to the Python executable.
        args.insert(0, sys.executable)
    import subprocess
    subprocess.check_call(args)

if __name__ == '__main__':
    main()
