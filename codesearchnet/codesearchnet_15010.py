def pep440_dev_version(self, verbose=False, non_local=False):
        """Return a PEP-440 dev version appendix to the main version number."""
        # Always return a timestamp
        pep440 = '.dev{:%Y%m%d%H%M}'.format(datetime.now())

        if not non_local:
            build_number = os.environ.get('BUILD_NUMBER', 'n/a')
            if build_number.isdigit():
                pep440 += '+ci.{}'.format(build_number)
                if verbose:
                    notify.info("Adding CI build ID #{} to version".format(build_number))

        return pep440