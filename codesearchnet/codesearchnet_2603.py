def register_metrics(self, context):
    """Registers metrics to context

    :param context: Topology Context
    """
    sys_config = system_config.get_sys_config()
    interval = float(sys_config[constants.HERON_METRICS_EXPORT_INTERVAL_SEC])
    collector = context.get_metrics_collector()
    super(ComponentMetrics, self).register_metrics(collector, interval)