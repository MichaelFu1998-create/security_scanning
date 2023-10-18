def _get_ckptmgr_process(self):
    ''' Get the command to start the checkpoint manager process'''

    ckptmgr_main_class = 'org.apache.heron.ckptmgr.CheckpointManager'

    ckptmgr_ram_mb = self.checkpoint_manager_ram / (1024 * 1024)
    ckptmgr_cmd = [os.path.join(self.heron_java_home, "bin/java"),
                   '-Xms%dM' % ckptmgr_ram_mb,
                   '-Xmx%dM' % ckptmgr_ram_mb,
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
                   '-XX:+UseConcMarkSweepGC',
                   '-Xloggc:log-files/gc.ckptmgr.log',
                   '-Djava.net.preferIPv4Stack=true',
                   '-cp',
                   self.checkpoint_manager_classpath,
                   ckptmgr_main_class,
                   '-t' + self.topology_name,
                   '-i' + self.topology_id,
                   '-c' + self.ckptmgr_ids[self.shard],
                   '-p' + self.checkpoint_manager_port,
                   '-f' + self.stateful_config_file,
                   '-o' + self.override_config_file,
                   '-g' + self.heron_internals_config_file]
    retval = {}
    retval[self.ckptmgr_ids[self.shard]] = Command(ckptmgr_cmd, self.shell_env)

    return retval