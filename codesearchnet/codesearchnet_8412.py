def trun_emph(trun):
    """Print essential info on"""

    if trun["conf"]["VERBOSE"] > 1:               # Print environment variables
        cij.emph("rnr:CONF {")
        for cvar in sorted(trun["conf"].keys()):
            cij.emph("  % 16s: %r" % (cvar, trun["conf"][cvar]))
        cij.emph("}")

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:INFO {")
        cij.emph("  OUTPUT: %r" % trun["conf"]["OUTPUT"])
        cij.emph("  yml_fpath: %r" % yml_fpath(trun["conf"]["OUTPUT"]))
        cij.emph("}")