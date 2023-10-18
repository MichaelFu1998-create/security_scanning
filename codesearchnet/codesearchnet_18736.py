def parse(self):
        """load the script and set the parser and argument info

        I feel that this is way too brittle to be used long term, I think it just
        might be best to import the stupid module, the thing I don't like about that
        is then we import basically everything, which seems bad?
        """
        if self.parsed: return

        self.callbacks = {}

        # search for main and any main_* callable objects
        regex = re.compile("^{}_?".format(self.function_name), flags=re.I)
        mains = set()
        body = self.body
        ast_tree = ast.parse(self.body, self.path)
        for n in ast_tree.body:
            if hasattr(n, 'name'):
                if regex.match(n.name):
                    mains.add(n.name)

            if hasattr(n, 'value'):
                ns = n.value
                if hasattr(ns, 'id'):
                    if regex.match(ns.id):
                        mains.add(ns.id)

            if hasattr(n, 'targets'):
                ns = n.targets[0]
                if hasattr(ns, 'id'):
                    if regex.match(ns.id):
                        mains.add(ns.id)

            if hasattr(n, 'names'):
                for ns in n.names:
                    if hasattr(ns, 'name'):
                        if regex.match(ns.name):
                            mains.add(ns.name)

                    if getattr(ns, 'asname', None):
                        if regex.match(ns.asname):
                            mains.add(ns.asname)

        if len(mains) > 0:
            module = self.module
            for function_name in mains:
                cb = getattr(module, function_name, None)
                if cb and callable(cb):
                    self.callbacks[function_name] = cb

        else:
            raise ParseError("no main function found")

        self.parsed = True
        return len(self.callbacks) > 0