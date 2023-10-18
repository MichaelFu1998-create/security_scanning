def satisfyTarget(self, target_name_and_version, update_installed=False, additional_config=None, install_missing=True):
        ''' Ensure that the specified target name (and optionally version,
            github ref or URL) is installed in the targets directory of the
            current component

            returns (derived_target, errors)
        '''
        # Target, , represent an installed target, internal
        from yotta.lib import target
        application_dir = None
        if self.isApplication():
            application_dir = self.path
        return target.getDerivedTarget(
                                target_name_and_version,
                                self.targetsPath(),
              install_missing = install_missing,
              application_dir = application_dir,
             update_installed = update_installed,
            additional_config = additional_config,
                   shrinkwrap = self.getShrinkwrap()
        )