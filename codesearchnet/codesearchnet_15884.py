def _feval(self, func_name, func_args=(), dname='', nout=0,
              timeout=None, stream_handler=None, store_as='', plot_dir=None):
        """Run the given function with the given args.
        """
        engine = self._engine
        if engine is None:
            raise Oct2PyError('Session is closed')

        # Set up our mat file paths.
        out_file = osp.join(self.temp_dir, 'writer.mat')
        out_file = out_file.replace(osp.sep, '/')
        in_file = osp.join(self.temp_dir, 'reader.mat')
        in_file = in_file.replace(osp.sep, '/')

        func_args = list(func_args)
        ref_indices = []
        for (i, value) in enumerate(func_args):
            if isinstance(value, OctavePtr):
                ref_indices.append(i + 1)
                func_args[i] = value.address
        ref_indices = np.array(ref_indices)

        # Save the request data to the output file.
        req = dict(func_name=func_name, func_args=tuple(func_args),
                   dname=dname or '', nout=nout,
                   store_as=store_as or '',
                   ref_indices=ref_indices)

        write_file(req, out_file, oned_as=self._oned_as,
                   convert_to_float=self.convert_to_float)

        # Set up the engine and evaluate the `_pyeval()` function.
        engine.stream_handler = stream_handler or self.logger.info
        if timeout is None:
            timeout = self.timeout

        try:
            engine.eval('_pyeval("%s", "%s");' % (out_file, in_file),
                        timeout=timeout)
        except KeyboardInterrupt as e:
            stream_handler(engine.repl.interrupt())
            raise
        except TIMEOUT:
            stream_handler(engine.repl.interrupt())
            raise Oct2PyError('Timed out, interrupting')
        except EOF:
            stream_handler(engine.repl.child.before)
            self.restart()
            raise Oct2PyError('Session died, restarting')

        # Read in the output.
        resp = read_file(in_file, self)
        if resp['err']:
            msg = self._parse_error(resp['err'])
            raise Oct2PyError(msg)

        result = resp['result'].ravel().tolist()
        if isinstance(result, list) and len(result) == 1:
            result = result[0]

        # Check for sentinel value.
        if (isinstance(result, Cell) and
                result.size == 1 and
                isinstance(result[0], string_types) and
                result[0] == '__no_value__'):
            result = None

        if plot_dir:
            self._engine.make_figures(plot_dir)

        return result