def make_zip_archive(self,
                         dst=None,
                         filters=all_true,
                         compress=True,
                         overwrite=False,
                         makedirs=False,
                         verbose=False):  # pragma: no cover
        """
        Make a zip archive.

        :param dst: output file path. if not given, will be automatically assigned.
        :param filters: custom path filter. By default it allows any file.
        :param compress: compress or not.
        :param overwrite: overwrite exists or not.
        :param verbose: display log or not.
        :return:
        """
        self.assert_exists()

        if dst is None:
            dst = self._auto_zip_archive_dst()
        else:
            dst = self.change(new_abspath=dst)

        if not dst.basename.lower().endswith(".zip"):
            raise ValueError("zip archive name has to be endswith '.zip'!")

        if dst.exists():
            if not overwrite:
                raise IOError("'%s' already exists!" % dst)

        if compress:
            compression = ZIP_DEFLATED
        else:
            compression = ZIP_STORED

        if not dst.parent.exists():
            if makedirs:
                os.makedirs(dst.parent.abspath)

        if verbose:
            msg = "Making zip archive for '%s' ..." % self
            print(msg)

        current_dir = os.getcwd()

        if self.is_dir():
            total_size = 0
            selected = list()
            for p in self.glob("**/*"):
                if filters(p):
                    selected.append(p)
                    total_size += p.size

            if verbose:
                msg = "Got {} files, total size is {}, compressing ...".format(
                    len(selected), repr_data_size(total_size),
                )
                print(msg)

            with ZipFile(dst.abspath, "w", compression) as f:
                os.chdir(self.abspath)
                for p in selected:
                    relpath = p.relative_to(self).__str__()
                    f.write(relpath)

        elif self.is_file():
            with ZipFile(dst.abspath, "w", compression) as f:
                os.chdir(self.parent.abspath)
                f.write(self.basename)

        os.chdir(current_dir)

        if verbose:
            msg = "Complete! Archive size is {}.".format(dst.size_in_text)
            print(msg)