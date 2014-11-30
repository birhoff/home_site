import os

from setuptools import setup, find_packages

PACKAGE_ROOT = '.'
PACKAGE_NAME = 'home_site'

# populate namespace with __version__
execfile(os.path.join(PACKAGE_ROOT, PACKAGE_NAME, 'version.py'))


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []

root_dir = os.path.abspath(os.path.dirname(__file__))

os.chdir(os.path.join(root_dir, PACKAGE_ROOT))


def data_files_filter(paths):
    return filter(lambda path: not path.endswith('.local'), paths)


def find_data_files(root, depth=0, maxdepth=4):
    if depth > maxdepth:
        return []
    data_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Ignore dirnames that start with '.'
        for i, dirname in enumerate(dirnames):
            if dirname.startswith('.'):
                del dirnames[i]
            elif os.path.islink(os.path.join(dirpath, dirname)):
                data_files.extend(find_data_files(os.path.join(dirpath, dirname), depth+1, maxdepth))
        if filenames and '__init__.py' not in filenames:
            data_files.extend(
                    path.split(os.path.sep, 1)[1] for path in
                        (os.path.join(dirpath, f) for f in filenames))
            #data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])
    return data_files

data_files = find_data_files(PACKAGE_NAME)

os.chdir(root_dir)

setup(
    name=PACKAGE_NAME,
    version=__version__,
    package_dir={
        '': PACKAGE_ROOT
    },
    packages=find_packages(
        PACKAGE_ROOT,
        exclude=()
    ),
    #scripts = ['say_hello.py'],

    package_data = {
        '': data_files_filter(data_files),
    },

    # Metadata
    author = "Kontantin Gladkikh",
    author_email = "birhoff@gmail.com",
    keywords = "kwrds",
)