def _extract_members(self, members, targetpath, pwd):
        """Extract the RarInfo objects 'members' to a physical
           file on the path targetpath.
        """
        archive = unrarlib.RAROpenArchiveDataEx(
            self.filename, mode=constants.RAR_OM_EXTRACT)
        handle = self._open(archive)

        password = pwd or self.pwd
        if password is not None:
            unrarlib.RARSetPassword(handle, b(password))

        try:
            rarinfo = self._read_header(handle)
            while rarinfo is not None:
                if rarinfo.filename in members:
                    self._process_current(
                        handle, constants.RAR_EXTRACT, targetpath)
                else:
                    self._process_current(handle, constants.RAR_SKIP)
                rarinfo = self._read_header(handle)
        except unrarlib.MissingPassword:
            raise RuntimeError("File is encrypted, password required")
        except unrarlib.BadPassword:
            raise RuntimeError("Bad password for File")
        except unrarlib.BadDataError:
            raise RuntimeError("File CRC Error")
        except unrarlib.UnrarException as e:
            raise BadRarFile("Bad RAR archive data: %s" % str(e))
        finally:
            self._close(handle)