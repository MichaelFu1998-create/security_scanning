def open(self, member, pwd=None):
        """Return file-like object for 'member'.

           'member' may be a filename or a RarInfo object.
        """
        if isinstance(member, RarInfo):
            member = member.filename

        archive = unrarlib.RAROpenArchiveDataEx(
            self.filename, mode=constants.RAR_OM_EXTRACT)
        handle = self._open(archive)

        password = pwd or self.pwd
        if password is not None:
            unrarlib.RARSetPassword(handle, b(password))

        # based on BrutuZ (https://github.com/matiasb/python-unrar/pull/4)
        # and Cubixmeister work
        data = _ReadIntoMemory()
        c_callback = unrarlib.UNRARCALLBACK(data._callback)
        unrarlib.RARSetCallback(handle, c_callback, 0)

        try:
            rarinfo = self._read_header(handle)
            while rarinfo is not None:
                if rarinfo.filename == member:
                    self._process_current(handle, constants.RAR_TEST)
                    break
                else:
                    self._process_current(handle, constants.RAR_SKIP)
                rarinfo = self._read_header(handle)

            if rarinfo is None:
                data = None

        except unrarlib.MissingPassword:
            raise RuntimeError("File is encrypted, password required")
        except unrarlib.BadPassword:
            raise RuntimeError("Bad password for File")
        except unrarlib.BadDataError:
            if password is not None:
                raise RuntimeError("File CRC error or incorrect password")
            else:
                raise RuntimeError("File CRC error")
        except unrarlib.UnrarException as e:
            raise BadRarFile("Bad RAR archive data: %s" % str(e))
        finally:
            self._close(handle)

        if data is None:
            raise KeyError('There is no item named %r in the archive' % member)

        # return file-like object
        return data.get_bytes()