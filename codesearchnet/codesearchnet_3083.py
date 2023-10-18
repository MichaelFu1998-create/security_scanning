def execute(self, js=None, use_compilation_plan=False):
        """executes javascript js in current context

        During initial execute() the converted js is cached for re-use. That means next time you
        run the same javascript snippet you save many instructions needed to parse and convert the
        js code to python code.

        This cache causes minor overhead (a cache dicts is updated) but the Js=>Py conversion process
        is typically expensive compared to actually running the generated python code.

        Note that the cache is just a dict, it has no expiration or cleanup so when running this
        in automated situations with vast amounts of snippets it might increase memory usage.
        """
        try:
            cache = self.__dict__['cache']
        except KeyError:
            cache = self.__dict__['cache'] = {}
        hashkey = hashlib.md5(js.encode('utf-8')).digest()
        try:
            compiled = cache[hashkey]
        except KeyError:
            code = translate_js(
                js, '', use_compilation_plan=use_compilation_plan)
            compiled = cache[hashkey] = compile(code, '<EvalJS snippet>',
                                                'exec')
        exec (compiled, self._context)