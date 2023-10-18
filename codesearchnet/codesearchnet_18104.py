def setup_passthroughs(self):
        """
        Inherit some functions from the components that we own. In particular,
        let's grab all functions that begin with `param_` so the super class
        knows how to get parameter groups. Also, take anything that is listed
        under Component.exports and rename with the category type, i.e.,
        SphereCollection.add_particle -> Component.obj_add_particle
        """
        self._nopickle = []

        for c in self.comps:
            # take all member functions that start with 'param_'
            funcs = inspect.getmembers(c, predicate=inspect.ismethod)
            for func in funcs:
                if func[0].startswith('param_'):
                    setattr(self, func[0], func[1])
                    self._nopickle.append(func[0])

            # add everything from exports
            funcs = c.exports()
            for func in funcs:
                newname = c.category + '_' + func.__func__.__name__
                setattr(self, newname, func)
                self._nopickle.append(newname)