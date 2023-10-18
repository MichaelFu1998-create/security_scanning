def execute_reports(
        config,
        path,
        collector,
        on_report_finish=None,
        output_file=None):
    """
    Executes the configured suite of issue reports.

    :param config: the TidyPy configuration to use
    :type config: dict
    :param path: that path to the project that was analyzed
    :type path: str
    :param collector: the issues to report
    :type collector: tidypy.Collector
    """

    reports = get_reports()
    for report in config.get('requested_reports', []):
        if report.get('type') and report['type'] in reports:
            cfg = config.get('report', {}).get(report['type'], {})
            cfg.update(report)
            reporter = reports[report['type']](
                cfg,
                path,
                output_file=output_file,
            )
            reporter.produce(collector)
            if on_report_finish:
                on_report_finish(report)