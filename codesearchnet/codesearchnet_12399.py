def run_cell(self, cell):
        """Run the Cell code using the IPython globals and locals

        Args:
            cell (str): Python code to be executed
        """
        globals = self.ipy_shell.user_global_ns
        locals = self.ipy_shell.user_ns
        globals.update({
            "__ipy_scope__": None,
        })
        try:
            with redirect_stdout(self.stdout):
                self.run(cell, globals, locals)
        except:
            self.code_error = True
            if self.options.debug:
                raise BdbQuit
        finally:
            self.finalize()