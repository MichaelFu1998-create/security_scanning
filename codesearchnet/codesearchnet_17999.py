def evaluate(self, comps, funcname='get', diffmap=None, **kwargs):
        """
        Calculate the output of a model. It is recommended that at some point
        before using `evaluate`, that you make sure the inputs are valid using
        :class:`~peri.models.Model.check_inputs`

        Parameters
        -----------
        comps : list of :class:`~peri.comp.comp.Component`
            Components which will be used to evaluate the model

        funcname : string (default: 'get')
            Name of the function which to evaluate for the components which
            represent their output. That is, when each component is used in the
            evaluation, it is really their ``attr(comp, funcname)`` which is used.

        diffmap : dictionary
            Extra mapping of derivatives or other symbols to extra variables.
            For example, the difference in a component has been evaluated as
            diff_obj so we set ``{'I': diff_obj}``

        ``**kwargs``:
            Arguments passed to ``funcname`` of component objects
        """
        evar = self.map_vars(comps, funcname, diffmap=diffmap)

        if diffmap is None:
            return eval(self.get_base_model(), evar)
        else:
            compname = list(diffmap.keys())[0]
            return eval(self.get_difference_model(compname), evar)