def sys_chdir(self, path):
        """
        chdir - Change current working directory
        :param int path: Pointer to path
        """
        path_str = self.current.read_string(path)
        logger.debug(f"chdir({path_str})")
        try:
            os.chdir(path_str)
            return 0
        except OSError as e:
            return e.errno