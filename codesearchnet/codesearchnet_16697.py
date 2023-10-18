def _update_data(self):
        """Update altfunc"""

        func = self.owner.formula.func
        codeobj = func.__code__
        name = func.__name__  # self.cells.name   # func.__name__
        namespace_impl = self.owner._namespace_impl.get_updated()
        namespace = namespace_impl.interfaces
        selfnode = get_node(self.owner, None, None)

        for name in self.owner.formula.srcnames:
            if name in namespace_impl and isinstance(
                namespace_impl[name], ReferenceImpl
            ):
                refnode = get_node(namespace_impl[name], None, None)
                self.owner.model.lexdep.add_path([selfnode, refnode])

        closure = func.__closure__  # None normally.
        if closure is not None:  # pytest fails without this.
            closure = create_closure(self.owner.interface)

        self.altfunc = FunctionType(
            codeobj, namespace, name=name, closure=closure
        )