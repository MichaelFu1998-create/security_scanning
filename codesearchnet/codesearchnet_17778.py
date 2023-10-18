def print_peak_memory(func,stream = None):
    """
    Print peak memory usage (in MB) of a function call
    
    :param func: Function to be called
    :param stream: Stream to write peak memory usage (defaults to stdout)  
    
    https://stackoverflow.com/questions/9850995/tracking-maximum-memory-usage-by-a-python-function
    """
    import time
    import psutil
    import os
    memory_denominator=1024**2
    memory_usage_refresh=0.05
    def wrapper(*args,**kwargs):
        from multiprocessing.pool import ThreadPool
        pool = ThreadPool(processes=1)
        process = psutil.Process(os.getpid())
        start_mem = process.memory_info().rss
        delta_mem = 0
        max_memory = 0
        async_result = pool.apply_async(func, args,kwargs)
        # do some other stuff in the main process
        while(not async_result.ready()):
            current_mem = process.memory_info().rss
            delta_mem = current_mem - start_mem
            if delta_mem > max_memory:
                max_memory = delta_mem
            # Check to see if the library call is complete
            time.sleep(memory_usage_refresh)
        
        return_val = async_result.get()  # get the return value from your function.
        max_memory /= memory_denominator
        if stream is not None:
            stream.write(str(max_memory))
        return return_val
    return wrapper