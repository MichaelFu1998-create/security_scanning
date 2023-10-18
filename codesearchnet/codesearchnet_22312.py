def render(self, match_string, new_string):
        """
        render template string to user string
        :param str match_string: template string,syntax: '___VAR___'
        :param str new_string: user string
        :return:
        """

        current_dir = self.options.dir

        # safe check,we don't allow handle system root and user root.
        if os.path.expanduser(current_dir) in ['/', os.path.expanduser("~")]:
            self.error("invalid directory", -1)
            pass

        def match_directory(path):
            """
            exclude indeed directory.

            .. note::

                this function will ignore in all depth.


            :param path:
            :return:
            """
            skip = False
            for include_dir in ['/%s/' % s for s in
                                self.exclude_directories]:
                if path.find(include_dir) > -1:
                    skip = True
                    break
                pass
            return skip

        # handle files detail first
        for v in os.walk(current_dir):
            # skip exclude directories in depth 1
            if os.path.basename(v[0]) in self.exclude_directories:
                continue
            if match_directory(v[0]):
                continue

            for base_name in v[2]:
                file_name = os.path.join(v[0], base_name)

                try:
                    with open(file_name, 'r') as fh:
                        buffer = fh.read()
                        buffer = buffer.replace(match_string, new_string)
                        pass

                    with open(file_name, 'w') as fh:
                        fh.write(buffer)
                        pass
                except UnicodeDecodeError:
                    # ignore binary files
                    continue

                pass
            pass

        # handle directory
        redo_directories = []
        redo_files = []

        for v in os.walk(current_dir):
            if os.path.basename(v[0]) in self.exclude_directories:
                continue
            if match_directory(v[0]):
                continue

            for sub_dir in v[1]:
                if match_string in sub_dir:
                    redo_directories.append(os.path.join(v[0], sub_dir))
                    pass

            for f in v[2]:
                if match_string in f:
                    redo_files.append(os.path.join(v[0], f))
                    pass
            pass

        redo_directories.reverse()
        redo_files.reverse()

        # redo files first
        for v in redo_files:
            dir_name = os.path.dirname(v)
            file_name = os.path.basename(v)
            shutil.move(v, os.path.join(
                dir_name,
                file_name.replace(match_string, new_string)))
            pass

        for v in redo_directories:
            shutil.move(v, v.replace(match_string, new_string))
            pass

        pass