def sys_rename(self, oldnamep, newnamep):
        """
        Rename filename `oldnamep` to `newnamep`.

        :param int oldnamep: pointer to oldname
        :param int newnamep: pointer to newname
        """
        oldname = self.current.read_string(oldnamep)
        newname = self.current.read_string(newnamep)

        ret = 0
        try:
            os.rename(oldname, newname)
        except OSError as e:
            ret = -e.errno

        return ret