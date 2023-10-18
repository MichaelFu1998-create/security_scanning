def _get_samples(self, samples):
    """
    Internal function. Prelude for each step() to read in perhaps
    non empty list of samples to process. Input is a list of sample names,
    output is a list of sample objects."""
    ## if samples not entered use all samples
    if not samples:
        samples = self.samples.keys()

    ## Be nice and allow user to pass in only one sample as a string,
    ## rather than a one element list. When you make the string into a list
    ## you have to wrap it in square braces or else list makes a list of
    ## each character individually.
    if isinstance(samples, str):
        samples = list([samples])

    ## if sample keys, replace with sample obj
    assert isinstance(samples, list), \
        "to subselect samples enter as a list, e.g., [A, B]."
    newsamples = [self.samples.get(key) for key in samples \
                  if self.samples.get(key)]
    strnewsamples = [i.name for i in newsamples]

    ## are there any samples that did not make it into the dict?
    badsamples = set(samples).difference(set(strnewsamples))
    if badsamples:
        outstring = ", ".join(badsamples)
        raise IPyradError(\
        "Unrecognized Sample name(s) not linked to {}: {}"\
        .format(self.name, outstring))

    ## require Samples
    assert newsamples, \
           "No Samples passed in and none in assembly {}".format(self.name)

    return newsamples