def mmPrettyPrintMetrics(metrics, sigFigs=5):
    """
    Returns pretty-printed table of metrics.

    @param metrics (list) Traces to print in table
    @param sigFigs (int)  Number of significant figures to print

    @return (string) Pretty-printed table of metrics.
    """
    assert len(metrics) > 0, "No metrics found"
    table = PrettyTable(["Metric", "mean", "standard deviation",
                         "min", "max", "sum", ])

    for metric in metrics:
      table.add_row([metric.prettyPrintTitle()] + metric.getStats())

    return table.get_string().encode("utf-8")