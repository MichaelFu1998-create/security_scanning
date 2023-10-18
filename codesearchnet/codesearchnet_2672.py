def _get_metrics_cache_cmd(self):
    ''' get the command to start the metrics manager processes '''
    metricscachemgr_main_class = 'org.apache.heron.metricscachemgr.MetricsCacheManager'

    metricscachemgr_cmd = [os.path.join(self.heron_java_home, 'bin/java'),
                           # We could not rely on the default -Xmx setting, which could be very big,
                           # for instance, the default -Xmx in Twitter mesos machine is around 18GB
                           '-Xmx1024M',
                           '-XX:+PrintCommandLineFlags',
                           '-verbosegc',
                           '-XX:+PrintGCDetails',
                           '-XX:+PrintGCTimeStamps',
                           '-XX:+PrintGCDateStamps',
                           '-XX:+PrintGCCause',
                           '-XX:+UseGCLogFileRotation',
                           '-XX:NumberOfGCLogFiles=5',
                           '-XX:GCLogFileSize=100M',
                           '-XX:+PrintPromotionFailure',
                           '-XX:+PrintTenuringDistribution',
                           '-XX:+PrintHeapAtGC',
                           '-XX:+HeapDumpOnOutOfMemoryError',
                           '-XX:+UseConcMarkSweepGC',
                           '-XX:+PrintCommandLineFlags',
                           '-Xloggc:log-files/gc.metricscache.log',
                           '-Djava.net.preferIPv4Stack=true',
                           '-cp',
                           self.metricscache_manager_classpath,
                           metricscachemgr_main_class,
                           "--metricscache_id", 'metricscache-0',
                           "--master_port", self.metricscache_manager_master_port,
                           "--stats_port", self.metricscache_manager_stats_port,
                           "--topology_name", self.topology_name,
                           "--topology_id", self.topology_id,
                           "--system_config_file", self.heron_internals_config_file,
                           "--override_config_file", self.override_config_file,
                           "--sink_config_file", self.metrics_sinks_config_file,
                           "--cluster", self.cluster,
                           "--role", self.role,
                           "--environment", self.environment]

    return Command(metricscachemgr_cmd, self.shell_env)