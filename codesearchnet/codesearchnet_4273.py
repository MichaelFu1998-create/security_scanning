def set_file_name(self, doc, name):
        """Raises OrderError if no package defined.
        """
        if self.has_package(doc):
            doc.package.files.append(file.File(name))
            # A file name marks the start of a new file instance.
            # The builder must be reset
            # FIXME: this state does not make sense
            self.reset_file_stat()
            return True
        else:
            raise OrderError('File::Name')