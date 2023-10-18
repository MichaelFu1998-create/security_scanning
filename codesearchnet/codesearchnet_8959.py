def _generate_contents(self, tar):
        """
        Adds configuration files to tarfile instance.

        :param tar: tarfile instance
        :returns: None
        """
        uci = self.render(files=False)
        # create a list with all the packages (and remove empty entries)
        packages = re.split('package ', uci)
        if '' in packages:
            packages.remove('')
        # create a file for each configuration package used
        for package in packages:
            lines = package.split('\n')
            package_name = lines[0]
            text_contents = '\n'.join(lines[2:])
            text_contents = 'package {0}\n\n{1}'.format(package_name, text_contents)
            self._add_file(tar=tar,
                           name='uci/{0}.conf'.format(package_name),
                           contents=text_contents)
        # prepare template context for install and uninstall scripts
        template_context = self._get_install_context()
        # add install.sh to included files
        self._add_install(template_context)
        # add uninstall.sh to included files
        self._add_uninstall(template_context)
        # add vpn up and down scripts
        self._add_openvpn_scripts()
        # add tc_script
        self._add_tc_script()