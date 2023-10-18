def _wait_process_std_out_err(self, name, process):
    ''' Wait for the termination of a process and log its stdout & stderr '''
    proc.stream_process_stdout(process, stdout_log_fn(name))
    process.wait()