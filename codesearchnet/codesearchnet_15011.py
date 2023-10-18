def get_egg_info(cfg, verbose=False):
    """Call 'setup egg_info' and return the parsed meta-data."""
    result = Bunch()
    setup_py = cfg.rootjoin('setup.py')
    if not os.path.exists(setup_py):
        return result

    egg_info = shell.capture("python {} egg_info".format(setup_py), echo=True if verbose else None)
    for info_line in egg_info.splitlines():
        if info_line.endswith('PKG-INFO'):
            pkg_info_file = info_line.split(None, 1)[1]
            result['__file__'] = pkg_info_file
            with io.open(pkg_info_file, encoding='utf-8') as handle:
                lastkey = None
                for line in handle:
                    if line.lstrip() != line:
                        assert lastkey, "Bad continuation in PKG-INFO file '{}': {}".format(pkg_info_file, line)
                        result[lastkey] += '\n' + line
                    else:
                        lastkey, value = line.split(':', 1)
                        lastkey = lastkey.strip().lower().replace('-', '_')
                        value = value.strip()
                        if lastkey in result:
                            try:
                                result[lastkey].append(value)
                            except AttributeError:
                                result[lastkey] = [result[lastkey], value]
                        else:
                            result[lastkey] = value

    for multikey in PKG_INFO_MULTIKEYS:
        if not isinstance(result.get(multikey, []), list):
            result[multikey] = [result[multikey]]

    return result