def eval(self, expression, use_compilation_plan=False):
        """evaluates expression in current context and returns its value"""
        code = 'PyJsEvalResult = eval(%s)' % json.dumps(expression)
        self.execute(code, use_compilation_plan=use_compilation_plan)
        return self['PyJsEvalResult']