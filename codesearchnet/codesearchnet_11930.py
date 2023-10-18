def needs_initrole(self, stop_on_error=False):
        """
        Returns true if the host does not exist at the expected location and may need
        to have its initial configuration set.
        Returns false if the host exists at the expected location.
        """

        ret = False

        target_host_present = self.is_present()

        if not target_host_present:
            default_host_present = self.is_present(self.env.default_hostname)
            if default_host_present:
                if self.verbose:
                    print('Target host missing and default host present so host init required.')
                ret = True
            else:
                if self.verbose:
                    print('Target host missing but default host also missing, '
                        'so no host init required.')
#                 if stop_on_error:
#                     raise Exception(
#                         'Both target and default hosts missing! '
#                         'Is the machine turned on and plugged into the network?')
        else:
            if self.verbose:
                print('Target host is present so no host init required.')

        return ret