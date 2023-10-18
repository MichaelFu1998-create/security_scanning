def _get_healthmgr_cmd(self):
    ''' get the command to start the topology health manager processes '''
    healthmgr_main_class = 'org.apache.heron.healthmgr.HealthManager'

    healthmgr_cmd = [os.path.join(self.heron_java_home, 'bin/java'),
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
                     '-Xloggc:log-files/gc.healthmgr.log',
                     '-Djava.net.preferIPv4Stack=true',
                     '-cp', self.health_manager_classpath,
                     healthmgr_main_class,
                     "--cluster", self.cluster,
                     "--role", self.role,
                     "--environment", self.environment,
                     "--topology_name", self.topology_name,
                     "--metricsmgr_port", self.metrics_manager_port]

    return Command(healthmgr_cmd, self.shell_env)