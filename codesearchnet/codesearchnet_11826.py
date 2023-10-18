def install_apt(self, fn=None, package_name=None, update=0, list_only=0):
        """
        Installs system packages listed in apt-requirements.txt.
        """
        r = self.local_renderer
        assert self.genv[ROLE]
        apt_req_fqfn = fn or (self.env.apt_requirments_fn and self.find_template(self.env.apt_requirments_fn))
        if not apt_req_fqfn:
            return []
        assert os.path.isfile(apt_req_fqfn)

        lines = list(self.env.apt_packages or [])
        for _ in open(apt_req_fqfn).readlines():
            if _.strip() and not _.strip().startswith('#') \
            and (not package_name or _.strip() == package_name):
                lines.extend(_pkg.strip() for _pkg in _.split(' ') if _pkg.strip())

        if list_only:
            return lines

        tmp_fn = r.write_temp_file('\n'.join(lines))
        apt_req_fqfn = tmp_fn

        if not self.genv.is_local:
            r.put(local_path=tmp_fn, remote_path=tmp_fn)
            apt_req_fqfn = self.genv.put_remote_path
        r.sudo('DEBIAN_FRONTEND=noninteractive apt-get -yq update --fix-missing')
        r.sudo('DEBIAN_FRONTEND=noninteractive apt-get -yq install `cat "%s" | tr "\\n" " "`' % apt_req_fqfn)