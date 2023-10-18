def get_thumbprint(self):
        """
        Calculates the current thumbprint of the item being tracked.
        """
        extensions = self.extensions.split(' ')
        name_str = ' -or '.join('-name "%s"' % ext for ext in extensions)
        cmd = 'find ' + self.base_dir + r' -type f \( ' + name_str + r' \) -exec md5sum {} \; | sort -k 2 | md5sum'
        return getoutput(cmd)