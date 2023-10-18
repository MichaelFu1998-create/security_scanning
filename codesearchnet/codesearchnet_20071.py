def get_author_and_version(package):
    """
    Return package author and version as listed in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    author = re.search("__author__ = ['\"]([^'\"]+)['\"]", init_py).group(1)
    version = re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)
    return author, version