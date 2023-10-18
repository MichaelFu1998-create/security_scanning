def pep440_dev_version(self, verbose=False, non_local=False):
        """ Return a PEP-440 dev version appendix to the main version number.

            Result is ``None`` if the workdir is in a release-ready state
            (i.e. clean and properly tagged).
        """
        version = capture("python setup.py --version", echo=verbose)
        if verbose:
            notify.info("setuptools version = '{}'".format(version))

        now = '{:%Y%m%d!%H%M}'.format(datetime.now())
        tag = capture("git describe --long --tags --dirty='!{}'".format(now), echo=verbose)
        if verbose:
            notify.info("git describe = '{}'".format(tag))
        try:
            tag, date, time = tag.split('!')
        except ValueError:
            date = time = ''
        tag, commits, short_hash = tag.rsplit('-', 3)
        label = tag
        if re.match(r"v[0-9]+(\.[0-9]+)*", label):
            label = label[1:]

        # Make a PEP-440 version appendix, the format is:
        # [N!]N(.N)*[{a|b|rc}N][.postN][.devN][+<local version label>]
        if commits == '0' and label == version:
            pep440 = None
        else:
            local_part = [
                re.sub(r"[^a-zA-Z0-9]+", '.', label).strip('.'),  # reduce to alphanum and dots
                short_hash,
                date + ('T' + time if time else ''),
            ]
            build_number = os.environ.get('BUILD_NUMBER', 'n/a')
            if build_number.isdigit():
                local_part.extend(['ci', build_number])
                if verbose:
                    notify.info("Adding CI build ID #{} to version".format(build_number))

            local_part = [i for i in local_part if i]
            pep440 = '.dev{}+{}'.format(commits, '.'.join(local_part).strip('.'))
            if non_local:
                pep440, _ = pep440.split('+', 1)

        return pep440