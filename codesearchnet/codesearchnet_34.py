def apply_stats(self, statsUpdates):
        """ compute stats and update/apply the new stats to the running average
        """

        def updateAccumStats():
            if self._full_stats_init:
                return tf.cond(tf.greater(self.sgd_step, self._cold_iter), lambda: tf.group(*self._apply_stats(statsUpdates, accumulate=True, accumulateCoeff=1. / self._stats_accum_iter)), tf.no_op)
            else:
                return tf.group(*self._apply_stats(statsUpdates, accumulate=True, accumulateCoeff=1. / self._stats_accum_iter))

        def updateRunningAvgStats(statsUpdates, fac_iter=1):
            # return tf.cond(tf.greater_equal(self.factor_step,
            # tf.convert_to_tensor(fac_iter)), lambda:
            # tf.group(*self._apply_stats(stats_list, varlist)), tf.no_op)
            return tf.group(*self._apply_stats(statsUpdates))

        if self._async_stats:
            # asynchronous stats update
            update_stats = self._apply_stats(statsUpdates)

            queue = tf.FIFOQueue(1, [item.dtype for item in update_stats], shapes=[
                                 item.get_shape() for item in update_stats])
            enqueue_op = queue.enqueue(update_stats)

            def dequeue_stats_op():
                return queue.dequeue()
            self.qr_stats = tf.train.QueueRunner(queue, [enqueue_op])
            update_stats_op = tf.cond(tf.equal(queue.size(), tf.convert_to_tensor(
                0)), tf.no_op, lambda: tf.group(*[dequeue_stats_op(), ]))
        else:
            # synchronous stats update
            update_stats_op = tf.cond(tf.greater_equal(
                self.stats_step, self._stats_accum_iter), lambda: updateRunningAvgStats(statsUpdates), updateAccumStats)
        self._update_stats_op = update_stats_op
        return update_stats_op