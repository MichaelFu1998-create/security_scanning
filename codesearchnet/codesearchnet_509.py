def validation_metrics(self):
        """A helper function to compute validation related metrics"""

        if (self._validation_iterator is None) or (self._validation_metrics is None):
            raise AttributeError('Validation is not setup.')

        n = 0.0
        metric_sums = [0.0] * len(self._validation_metrics)
        self._sess.run(self._validation_iterator.initializer)
        while True:
            try:
                metrics = self._sess.run(self._validation_metrics)
                for i, m in enumerate(metrics):
                    metric_sums[i] += m
                n += 1.0
            except tf.errors.OutOfRangeError:
                break
        for i, m in enumerate(metric_sums):
            metric_sums[i] = metric_sums[i] / n
        return zip(self._validation_metrics, metric_sums)