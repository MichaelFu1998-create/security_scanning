def _run_command(self, *args, **kwargs):
        """Execute the command; see the docs for __call__.

        :Returns: a tuple of the *results* tuple ``(rc, stdout, stderr)`` and
                  the :class:`Popen` instance.
        """
        # hack to run command WITHOUT input (-h...) even though user defined
        # input (should have named it "ignore_input" with opposite values...)
        use_input = kwargs.pop('use_input', True)

        # logic for capturing output (see docs on I/O and the flags)
        capturefile = None
        if environment.flags['capture_output'] is True:
            # capture into Python vars (see subprocess.Popen.communicate())
            kwargs.setdefault('stderr', PIPE)
            kwargs.setdefault('stdout', PIPE)
        elif environment.flags['capture_output'] == "file":
            if 'stdout' in kwargs and 'stderr' in kwargs:
                pass
            else:
                # XXX: not race or thread proof; potentially many commands write to the same file
                fn = environment.flags['capture_output_filename']
                capturefile = file(fn, "w")   # overwrite (clobber) capture file
                if 'stdout' in kwargs and 'stderr' not in kwargs:
                    # special case of stdout used by code but stderr should be captured to file
                    kwargs.setdefault('stderr', capturefile)
                else:
                    # merge stderr with stdout and write stdout to file
                    # (stderr comes *before* stdout in capture file, could split...)
                    kwargs.setdefault('stderr', STDOUT)
                    kwargs.setdefault('stdout', capturefile)

        try:
            p = self.Popen(*args, **kwargs)
            out, err = p.communicate(use_input=use_input) # special Popen knows input!
        except:
            if capturefile is not None:
                logger.error("Use captured command output in %r for diagnosis.", capturefile)
            raise
        finally:
            if capturefile is not None:
                capturefile.close()
        rc = p.returncode
        return (rc, out, err), p