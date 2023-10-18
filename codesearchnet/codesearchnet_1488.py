def mmPrettyPrintTraces(traces, breakOnResets=None):
    """
    Returns pretty-printed table of traces.

    @param traces (list) Traces to print in table
    @param breakOnResets (BoolsTrace) Trace of resets to break table on

    @return (string) Pretty-printed table of traces.
    """
    assert len(traces) > 0, "No traces found"
    table = PrettyTable(["#"] + [trace.prettyPrintTitle() for trace in traces])

    for i in xrange(len(traces[0].data)):
      if breakOnResets and breakOnResets.data[i]:
        table.add_row(["<reset>"] * (len(traces) + 1))
      table.add_row([i] +
        [trace.prettyPrintDatum(trace.data[i]) for trace in traces])

    return table.get_string().encode("utf-8")