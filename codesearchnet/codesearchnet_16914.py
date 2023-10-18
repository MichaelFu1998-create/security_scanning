def nearest(self, ver):
        """
        Retrieve the official version nearest the one given.
        """
        if not isinstance(ver, Version):
            ver = Version(ver)

        if ver in OFFICIAL_VERSIONS:
            return ver

        # We might not have an exact match for that.
        # See if we have one that's newer than the grid we're looking at.
        versions = list(OFFICIAL_VERSIONS)
        versions.sort(reverse=True)
        best = None
        for candidate in versions:
            # Due to ambiguities, we might have an exact match and not know it.
            # '2.0' will not hash to the same value as '2.0.0', but both are
            # equivalent.
            if candidate == ver:
                # We can't beat this, make a note of the match for later
                return candidate

            # If we have not seen a better candidate, and this is older
            # then we may have to settle for that.
            if (best is None) and (candidate < ver):
                warnings.warn('This version of hszinc does not yet '\
                            'support version %s, please seek a newer version '\
                            'or file a bug.  Closest (older) version supported is %s.'\
                            % (ver, candidate))
                return candidate

            # Probably the best so far, but see if we can go closer
            if candidate > ver:
                best = candidate

        # Unhappy path, no best option?  This should not happen.
        assert best is not None
        warnings.warn('This version of hszinc does not yet '\
                    'support version %s, please seek a newer version '\
                    'or file a bug.  Closest (newer) version supported is %s.'\
                    % (ver, best))
        return best