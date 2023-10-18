def put(self, metrics):
        """
        Put metrics to cloudwatch. Metric shoult be instance or list of
        instances of CloudWatchMetric
        """
        if type(metrics) == list:
            for metric in metrics:
                self.c.put_metric_data(**metric)
        else:
            self.c.put_metric_data(**metrics)