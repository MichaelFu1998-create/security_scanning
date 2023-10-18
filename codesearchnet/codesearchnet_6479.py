def clear_cached_data(self):
        """Clear the internal bluetooth device cache.  This is useful if a device
        changes its state like name and it can't be detected with the new state
        anymore.  WARNING: This will delete some files underneath the running user's
        ~/Library/Preferences/ folder!

        See this Stackoverflow question for information on what the function does:
        http://stackoverflow.com/questions/20553957/how-can-i-clear-the-corebluetooth-cache-on-macos
        """
        # Turn off bluetooth.
        if self._adapter.is_powered:
            self._adapter.power_off()
        # Delete cache files and suppress any stdout/err output.
        with open(os.devnull, 'w') as devnull:
            subprocess.call('rm ~/Library/Preferences/com.apple.Bluetooth.plist',
                            shell=True, stdout=devnull, stderr=subprocess.STDOUT)
            subprocess.call('rm ~/Library/Preferences/ByHost/com.apple.Bluetooth.*.plist',
                            shell=True, stdout=devnull, stderr=subprocess.STDOUT)