def execute_debug(self, js):
        """executes javascript js in current context
        as opposed to the (faster) self.execute method, you can use your regular debugger
        to set breakpoints and inspect the generated python code
        """
        code = translate_js(js, '')
        # make sure you have a temp folder:
        filename = 'temp' + os.sep + '_' + hashlib.md5(
            code.encode("utf-8")).hexdigest() + '.py'
        try:
            with open(filename, mode='w') as f:
                f.write(code)
            with open(filename, "r") as f:
                pyCode = compile(f.read(), filename, 'exec')
                exec(pyCode, self._context)
                
        except Exception as err:
            raise err
        finally:
            os.remove(filename)
            try:
                os.remove(filename + 'c')
            except:
                pass