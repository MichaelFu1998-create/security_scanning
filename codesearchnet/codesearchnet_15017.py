def workdir_is_clean(self, quiet=False):
        """ Check for uncommitted changes, return `True` if everything is clean.

            Inspired by http://stackoverflow.com/questions/3878624/.
        """
        # Update the index
        self.run('git update-index -q --ignore-submodules --refresh', **RUN_KWARGS)
        unchanged = True

        # Disallow unstaged changes in the working tree
        try:
            self.run('git diff-files --quiet --ignore-submodules --', report_error=False, **RUN_KWARGS)
        except exceptions.Failure:
            unchanged = False
            if not quiet:
                notify.warning('You have unstaged changes!')
                self.run('git diff-files --name-status -r --ignore-submodules -- >&2', **RUN_KWARGS)

        # Disallow uncommitted changes in the index
        try:
            self.run('git diff-index --cached --quiet HEAD --ignore-submodules --', report_error=False, **RUN_KWARGS)
        except exceptions.Failure:
            unchanged = False
            if not quiet:
                notify.warning('Your index contains uncommitted changes!')
                self.run('git diff-index --cached --name-status -r --ignore-submodules HEAD -- >&2', **RUN_KWARGS)

        return unchanged