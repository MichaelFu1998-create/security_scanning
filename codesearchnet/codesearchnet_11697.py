def md5sum(self, filename, use_sudo=False):
        """
        Compute the MD5 sum of a file.
        """
        func = use_sudo and run_as_root or self.run
        with self.settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
            # Linux (LSB)
            if exists(u'/usr/bin/md5sum'):
                res = func(u'/usr/bin/md5sum %(filename)s' % locals())
            # BSD / OS X
            elif exists(u'/sbin/md5'):
                res = func(u'/sbin/md5 -r %(filename)s' % locals())
            # SmartOS Joyent build
            elif exists(u'/opt/local/gnu/bin/md5sum'):
                res = func(u'/opt/local/gnu/bin/md5sum %(filename)s' % locals())
            # SmartOS Joyent build
            # (the former doesn't exist, at least on joyent_20130222T000747Z)
            elif exists(u'/opt/local/bin/md5sum'):
                res = func(u'/opt/local/bin/md5sum %(filename)s' % locals())
            # Try to find ``md5sum`` or ``md5`` on ``$PATH`` or abort
            else:
                md5sum = func(u'which md5sum')
                md5 = func(u'which md5')
                if exists(md5sum):
                    res = func('%(md5sum)s %(filename)s' % locals())
                elif exists(md5):
                    res = func('%(md5)s %(filename)s' % locals())
                else:
                    abort('No MD5 utility was found on this system.')

        if res.succeeded:
            _md5sum = res
        else:
            warn(res)
            _md5sum = None

        if isinstance(_md5sum, six.string_types):
            _md5sum = _md5sum.strip().split('\n')[-1].split()[0]

        return _md5sum