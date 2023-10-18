def get_package_list(self):
        """
        Returns a list of all required packages.
        """
        os_version = self.os_version # OS(type=LINUX, distro=UBUNTU, release='14.04')
        self.vprint('os_version:', os_version)

        # Lookup legacy package list.
        # OS: [package1, package2, ...],
        req_packages1 = self.required_system_packages
        if req_packages1:
            deprecation('The required_system_packages attribute is deprecated, '
                'use the packager_system_packages property instead.')

        # Lookup new package list.
        # OS: [package1, package2, ...],
        req_packages2 = self.packager_system_packages

        patterns = [
            (os_version.type, os_version.distro, os_version.release),
            (os_version.distro, os_version.release),
            (os_version.type, os_version.distro),
            (os_version.distro,),
            os_version.distro,
        ]
        self.vprint('req_packages1:', req_packages1)
        self.vprint('req_packages2:', req_packages2)
        package_list = None
        found = False
        for pattern in patterns:
            self.vprint('pattern:', pattern)
            for req_packages in (req_packages1, req_packages2):
                if pattern in req_packages:
                    package_list = req_packages[pattern]
                    found = True
                    break
        if not found:
            print('Warning: No operating system pattern found for %s' % (os_version,))
        self.vprint('package_list:', package_list)
        return package_list