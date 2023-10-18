def check_for_change(self):
        """
        Determines if a new release has been made.
        """
        r = self.local_renderer
        lm = self.last_manifest
        last_fingerprint = lm.fingerprint
        current_fingerprint = self.get_target_geckodriver_version_number()
        self.vprint('last_fingerprint:', last_fingerprint)
        self.vprint('current_fingerprint:', current_fingerprint)
        if last_fingerprint != current_fingerprint:
            print('A new release is available. %s' % self.get_most_recent_version())
            return True
        print('No updates found.')
        return False