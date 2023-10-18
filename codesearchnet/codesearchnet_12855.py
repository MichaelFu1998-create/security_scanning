def set_params(self, param, newvalue):
        """
        Set a parameter to a new value. Raises error if newvalue is wrong type.

        Note
        ----
        Use [Assembly].get_params() to see the parameter values currently
        linked to the Assembly object.

        Parameters
        ----------
        param : int or str
            The index (e.g., 1) or string name (e.g., "project_dir")
            for the parameter that will be changed.

        newvalue : int, str, or tuple
            The new value for the parameter selected for `param`. Use
            `ipyrad.get_params_info()` to get further information about
            a given parameter. If the wrong type is entered for newvalue
            (e.g., a str when it should be an int), an error will be raised.
            Further information about each parameter is also available
            in the documentation.

        Examples
        --------
        ## param 'project_dir' takes only a str as input
        [Assembly].set_params('project_dir', 'new_directory')

        ## param 'restriction_overhang' must be a tuple or str, if str it is 
        ## converted to a tuple with the second entry empty.
        [Assembly].set_params('restriction_overhang', ('CTGCAG', 'CCGG')

        ## param 'max_shared_Hs_locus' can be an int or a float:
        [Assembly].set_params('max_shared_Hs_locus', 0.25)

        """

        ## this includes current params and some legacy params for conversion
        legacy_params = ["edit_cutsites", "trim_overhang"]
        current_params = self.paramsdict.keys()
        allowed_params = current_params + legacy_params

        ## require parameter recognition
        #if not ((param in range(50)) or \
        #        (param in [str(i) for i in range(50)]) or \
        #        (param in allowed_params)):
        if not param in allowed_params:
            raise IPyradParamsError("Parameter key not recognized: {}"\
                                    .format(param))

        ## make string
        param = str(param)
        ## get index if param is keyword arg (this index is now zero based!)
        if len(param) < 3:
            param = self.paramsdict.keys()[int(param)]

        ## run assertions on new param
        try:
            self = _paramschecker(self, param, newvalue)

        except Exception as inst:
            raise IPyradWarningExit(BAD_PARAMETER\
                                    .format(param, inst, newvalue))