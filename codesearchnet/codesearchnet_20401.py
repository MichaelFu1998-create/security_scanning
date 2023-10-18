def all_package_versions(package):
        """ All versions for package """
        info = PyPI.package_info(package)
        return info and sorted(info['releases'].keys(), key=lambda x: x.split(), reverse=True) or []