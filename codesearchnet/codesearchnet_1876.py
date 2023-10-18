def _MakeParallelBenchmark(p, work_func, *args):
  """Create and return a benchmark that runs work_func p times in parallel."""
  def Benchmark(b):  # pylint: disable=missing-docstring
    e = threading.Event()
    def Target():
      e.wait()
      for _ in xrange(b.N / p):
        work_func(*args)
    threads = []
    for _ in xrange(p):
      t = threading.Thread(target=Target)
      t.start()
      threads.append(t)
    b.ResetTimer()
    e.set()
    for t in threads:
      t.join()
  return Benchmark