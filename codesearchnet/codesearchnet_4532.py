def monitor(pid, task_id, monitoring_hub_url, run_id, sleep_dur=10):
    """Internal
    Monitors the Parsl task's resources by pointing psutil to the task's pid and watching it and its children.
    """
    import psutil

    radio = UDPRadio(monitoring_hub_url,
                     source_id=task_id)

    # these values are simple to log. Other information is available in special formats such as memory below.
    simple = ["cpu_num", 'cpu_percent', 'create_time', 'cwd', 'exe', 'memory_percent', 'nice', 'name', 'num_threads', 'pid', 'ppid', 'status', 'username']
    # values that can be summed up to see total resources used by task process and its children
    summable_values = ['cpu_percent', 'memory_percent', 'num_threads']

    pm = psutil.Process(pid)
    pm.cpu_percent()

    first_msg = True

    while True:
        try:
            d = {"psutil_process_" + str(k): v for k, v in pm.as_dict().items() if k in simple}
            d["run_id"] = run_id
            d["task_id"] = task_id
            d['resource_monitoring_interval'] = sleep_dur
            d['first_msg'] = first_msg
            d['timestamp'] = datetime.datetime.now()
            children = pm.children(recursive=True)
            d["psutil_cpu_count"] = psutil.cpu_count()
            d['psutil_process_memory_virtual'] = pm.memory_info().vms
            d['psutil_process_memory_resident'] = pm.memory_info().rss
            d['psutil_process_time_user'] = pm.cpu_times().user
            d['psutil_process_time_system'] = pm.cpu_times().system
            d['psutil_process_children_count'] = len(children)
            try:
                d['psutil_process_disk_write'] = pm.io_counters().write_bytes
                d['psutil_process_disk_read'] = pm.io_counters().read_bytes
            except psutil._exceptions.AccessDenied:
                # occassionally pid temp files that hold this information are unvailable to be read so set to zero
                d['psutil_process_disk_write'] = 0
                d['psutil_process_disk_read'] = 0
            for child in children:
                for k, v in child.as_dict(attrs=summable_values).items():
                    d['psutil_process_' + str(k)] += v
                d['psutil_process_time_user'] += child.cpu_times().user
                d['psutil_process_time_system'] += child.cpu_times().system
                d['psutil_process_memory_virtual'] += child.memory_info().vms
                d['psutil_process_memory_resident'] += child.memory_info().rss
                try:
                    d['psutil_process_disk_write'] += child.io_counters().write_bytes
                    d['psutil_process_disk_read'] += child.io_counters().read_bytes
                except psutil._exceptions.AccessDenied:
                    # occassionally pid temp files that hold this information are unvailable to be read so add zero
                    d['psutil_process_disk_write'] += 0
                    d['psutil_process_disk_read'] += 0

        finally:
            radio.send(MessageType.TASK_INFO, task_id, d)
            time.sleep(sleep_dur)
            first_msg = False