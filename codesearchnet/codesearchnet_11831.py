def list_required(self, type=None, service=None): # pylint: disable=redefined-builtin
        """
        Displays all packages required by the current role
        based on the documented services provided.
        """
        from burlap.common import (
            required_system_packages,
            required_python_packages,
            required_ruby_packages,
        )
        service = (service or '').strip().upper()
        type = (type or '').lower().strip()
        assert not type or type in PACKAGE_TYPES, 'Unknown package type: %s' % (type,)
        packages_set = set()
        packages = []
        version = self.os_version

        for _service, satchel in self.all_other_enabled_satchels.items():

            _service = _service.strip().upper()
            if service and service != _service:
                continue

            _new = []

            if not type or type == SYSTEM:

                #TODO:deprecated, remove
                _new.extend(required_system_packages.get(
                    _service, {}).get((version.distro, version.release), []))

                try:
                    _pkgs = satchel.packager_system_packages
                    if self.verbose:
                        print('pkgs:')
                        pprint(_pkgs, indent=4)
                    for _key in [(version.distro, version.release), version.distro]:
                        if self.verbose:
                            print('checking key:', _key)
                        if _key in _pkgs:
                            if self.verbose:
                                print('satchel %s requires:' % satchel, _pkgs[_key])
                            _new.extend(_pkgs[_key])
                            break
                except AttributeError:
                    pass

            if not type or type == PYTHON:

                #TODO:deprecated, remove
                _new.extend(required_python_packages.get(
                    _service, {}).get((version.distro, version.release), []))

                try:
                    _pkgs = satchel.packager_python_packages
                    for _key in [(version.distro, version.release), version.distro]:
                        if _key in _pkgs:
                            _new.extend(_pkgs[_key])
                except AttributeError:
                    pass
                print('_new:', _new)

            if not type or type == RUBY:

                #TODO:deprecated, remove
                _new.extend(required_ruby_packages.get(
                    _service, {}).get((version.distro, version.release), []))

            for _ in _new:
                if _ in packages_set:
                    continue
                packages_set.add(_)
                packages.append(_)
        if self.verbose:
            for package in sorted(packages):
                print('package:', package)
        return packages