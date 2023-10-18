def run(self, halt_on_nonzero=True, quiet=False, q=False, streaming=False):
        """
        After building your commands, call `run()` to have your code executed.
        """
        commands = str(self)
        if not (quiet or q):
            self._echo.cmd(commands)

        env = self._context[0].get('env', {}) if len(self._context) > 0 else os.environ
        executable = self.current_context.get('executable')
        try:
            process = subprocess.Popen(commands,
                                       bufsize=1,
                                       shell=True,
                                       env=env,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       executable=executable,
                                       universal_newlines=True)
            result = Result(process, commands, self._context, streaming, halt_on_nonzero=halt_on_nonzero)

        except Exception as e:
            result = Result(None, commands, self._context, exception=e)
            result.dump_exception()
            if halt_on_nonzero:
                raise e
                
        finally:
            self.clear()
        
        return result