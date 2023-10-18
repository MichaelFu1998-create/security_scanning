def install_plugin(self, dir, entry_script=None):
        """
        Install *Vim* plugin.

        :param string dir: the root directory contains *Vim* script
        :param string entry_script: path to the initializing script
        """
        self.runtimepath.append(dir)
        if entry_script is not None:
            self.command('runtime! {0}'.format(entry_script), False)