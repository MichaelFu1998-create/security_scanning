def _samples_precheck(self, samples, mystep, force):
        """ Return a list of samples that are actually ready for the next step.
            Each step runs this prior to calling run, makes it easier to
            centralize and normalize how each step is checking sample states.
            mystep is the state produced by the current step.
        """
        subsample = []
        ## filter by state
        for sample in samples:
            if sample.stats.state < mystep - 1:
                LOGGER.debug("Sample {} not in proper state."\
                             .format(sample.name))
            else:
                subsample.append(sample)
        return subsample