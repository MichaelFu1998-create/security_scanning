def link_file(self, path, prefixed_path, source_storage):
        """
        Attempt to link ``path``
        """
        # Skip this file if it was already copied earlier
        if prefixed_path in self.symlinked_files:
            return self.log("Skipping '%s' (already linked earlier)" % path)
        # Delete the target file if needed or break
        if not self.delete_file(path, prefixed_path, source_storage):
            return
        # The full path of the source file
        source_path = source_storage.path(path)
        # Finally link the file
        if self.dry_run:
            self.log("Pretending to link '%s'" % source_path, level=1)
        else:
            self.log("Linking '%s'" % source_path, level=1)
            full_path = self.storage.path(prefixed_path)
            try:
                os.makedirs(os.path.dirname(full_path))
            except OSError:
                pass
            try:
                if os.path.lexists(full_path):
                    os.unlink(full_path)
                os.symlink(source_path, full_path)
            except AttributeError:
                import platform
                raise CommandError("Symlinking is not supported by Python %s." %
                                   platform.python_version())
            except NotImplementedError:
                import platform
                raise CommandError("Symlinking is not supported in this "
                                   "platform (%s)." % platform.platform())
            except OSError as e:
                raise CommandError(e)
        if prefixed_path not in self.symlinked_files:
            self.symlinked_files.append(prefixed_path)