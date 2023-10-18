def start(self, builddir, program, forward_args):
        ''' Launch the specified program. Uses the `start` script if specified
            by the target, attempts to run it natively if that script is not
            defined.
        '''
        child = None
        try:
            prog_path = self.findProgram(builddir, program)
            if prog_path is None:
                return

            start_env, start_vars = self.buildProgEnvAndVars(prog_path, builddir)
            if self.getScript('start'):
                cmd = [
                    os.path.expandvars(string.Template(x).safe_substitute(**start_vars))
                    for x in self.getScript('start')
                ] + forward_args
            else:
                cmd = shlex.split('./' + prog_path) + forward_args

            logger.debug('starting program: %s', cmd)
            child = subprocess.Popen(
                cmd, cwd = builddir, env = start_env
            )
            child.wait()
            if child.returncode:
                return "process exited with status %s" % child.returncode
            child = None
        except OSError as e:
            import errno
            if e.errno == errno.ENOEXEC:
                return ("the program %s cannot be run (perhaps your target "+
                        "needs to define a 'start' script to start it on its "
                        "intended execution target?)") % prog_path
        finally:
            if child is not None:
                _tryTerminate(child)