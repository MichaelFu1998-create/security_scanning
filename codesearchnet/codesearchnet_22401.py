def assert_equal_files(self, obtained_fn, expected_fn, fix_callback=lambda x:x, binary=False, encoding=None):
        '''
        Compare two files contents. If the files differ, show the diff and write a nice HTML
        diff file into the data directory.

        Searches for the filenames both inside and outside the data directory (in that order).

        :param unicode obtained_fn: basename to obtained file into the data directory, or full path.

        :param unicode expected_fn: basename to expected file into the data directory, or full path.

        :param bool binary:
            Thread both files as binary files.

        :param unicode encoding:
            File's encoding. If not None, contents obtained from file will be decoded using this
            `encoding`.

        :param callable fix_callback:
            A callback to "fix" the contents of the obtained (first) file.
            This callback receives a list of strings (lines) and must also return a list of lines,
            changed as needed.
            The resulting lines will be used to compare with the contents of expected_fn.

        :param bool binary:
            .. seealso:: zerotk.easyfs.GetFileContents
        '''
        import os
        from zerotk.easyfs import GetFileContents, GetFileLines

        __tracebackhide__ = True
        import io

        def FindFile(filename):
            # See if this path exists in the data dir
            data_filename = self.get_filename(filename)
            if os.path.isfile(data_filename):
                return data_filename

            # If not, we might have already received a full path
            if os.path.isfile(filename):
                return filename

            # If we didn't find anything, raise an error
            from ._exceptions import MultipleFilesNotFound
            raise MultipleFilesNotFound([filename, data_filename])

        obtained_fn = FindFile(obtained_fn)
        expected_fn = FindFile(expected_fn)

        if binary:
            obtained_lines = GetFileContents(obtained_fn, binary=True)
            expected_lines = GetFileContents(expected_fn, binary=True)
            assert obtained_lines == expected_lines
        else:
            obtained_lines = fix_callback(GetFileLines(obtained_fn, encoding=encoding))
            expected_lines = GetFileLines(expected_fn, encoding=encoding)

            if obtained_lines != expected_lines:
                html_fn = os.path.splitext(obtained_fn)[0] + '.diff.html'
                html_diff = self._generate_html_diff(
                    expected_fn, expected_lines, obtained_fn, obtained_lines)
                with io.open(html_fn, 'w') as f:
                    f.write(html_diff)

                import difflib
                diff = ['FILES DIFFER:', obtained_fn, expected_fn]
                diff += ['HTML DIFF: %s' % html_fn]
                diff += difflib.context_diff(obtained_lines, expected_lines)
                raise AssertionError('\n'.join(diff) + '\n')