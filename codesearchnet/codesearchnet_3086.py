def eval_debug(self, expression):
        """evaluates expression in current context and returns its value
        as opposed to the (faster) self.execute method, you can use your regular debugger
        to set breakpoints and inspect the generated python code
        """
        code = 'PyJsEvalResult = eval(%s)' % json.dumps(expression)
        self.execute_debug(code)
        return self['PyJsEvalResult']