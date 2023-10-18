def install_yum(self, fn=None, package_name=None, update=0, list_only=0):
        """
        Installs system packages listed in yum-requirements.txt.
        """
        assert self.genv[ROLE]
        yum_req_fn = fn or self.find_template(self.genv.yum_requirments_fn)
        if not yum_req_fn:
            return []
        assert os.path.isfile(yum_req_fn)
        update = int(update)
        if list_only:
            return [
                _.strip() for _ in open(yum_req_fn).readlines()
                if _.strip() and not _.strip.startswith('#')
                and (not package_name or _.strip() == package_name)
            ]
        if update:
            self.sudo_or_dryrun('yum update --assumeyes')
        if package_name:
            self.sudo_or_dryrun('yum install --assumeyes %s' % package_name)
        else:
            if self.genv.is_local:
                self.put_or_dryrun(local_path=yum_req_fn)
                yum_req_fn = self.genv.put_remote_fn
            self.sudo_or_dryrun('yum install --assumeyes $(cat %(yum_req_fn)s)' % yum_req_fn)