def _get_metricsmgr_cmd(self, metricsManagerId, sink_config_file, port):
    ''' get the command to start the metrics manager processes '''
    metricsmgr_main_class = 'org.apache.heron.metricsmgr.MetricsManager'

    metricsmgr_cmd = [os.path.join(self.heron_java_home, 'bin/java'),
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
                      '-Xloggc:log-files/gc.metricsmgr.log',
                      '-Djava.net.preferIPv4Stack=true',
                      '-cp',
                      self.metrics_manager_classpath,
                      metricsmgr_main_class,
                      '--id=' + metricsManagerId,
                      '--port=' + str(port),
                      '--topology=' + self.topology_name,
                      '--cluster=' + self.cluster,
                      '--role=' + self.role,
                      '--environment=' + self.environment,
                      '--topology-id=' + self.topology_id,
                      '--system-config-file=' + self.heron_internals_config_file,
                      '--override-config-file=' + self.override_config_file,
                      '--sink-config-file=' + sink_config_file]

    return Command(metricsmgr_cmd, self.shell_env)