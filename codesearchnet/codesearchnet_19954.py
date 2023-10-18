def qdel_batch(self):
        """
        Runs qdel command to remove all remaining queued jobs using
        the <batch_name>* pattern . Necessary when StopIteration is
        raised with scheduled jobs left on the queue.
        Returns exit-code of qdel.
        """
        p = subprocess.Popen(['qdel', '%s_%s*' % (self.batch_name,
                                                  self.job_timestamp)],
                             stdout=subprocess.PIPE)
        (stdout, stderr) = p.communicate()
        return p.poll()