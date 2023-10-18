def _compatible_params_check(self):
        """ check for mindepths after all params are set, b/c doing it while each
        is being set becomes complicated """

        ## do not allow statistical < majrule
        val1 = self.paramsdict["mindepth_statistical"]
        val2 = self.paramsdict['mindepth_majrule']
        if val1 < val2:
            msg = """
    Warning: mindepth_statistical cannot not be < mindepth_majrule.
    Forcing mindepth_majrule = mindepth_statistical = {}
    """.format(val1)
            LOGGER.warning(msg)
            print(msg)
            self.paramsdict["mindepth_majrule"] = val1