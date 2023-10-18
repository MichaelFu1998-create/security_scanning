def computeStatsEigen(self):
        """ compute the eigen decomp using copied var stats to avoid concurrent read/write from other queue """
        # TO-DO: figure out why this op has delays (possibly moving
        # eigenvectors around?)
        with tf.device('/cpu:0'):
            def removeNone(tensor_list):
                local_list = []
                for item in tensor_list:
                    if item is not None:
                        local_list.append(item)
                return local_list

            def copyStats(var_list):
                print("copying stats to buffer tensors before eigen decomp")
                redundant_stats = {}
                copied_list = []
                for item in var_list:
                    if item is not None:
                        if item not in redundant_stats:
                            if self._use_float64:
                                redundant_stats[item] = tf.cast(
                                    tf.identity(item), tf.float64)
                            else:
                                redundant_stats[item] = tf.identity(item)
                        copied_list.append(redundant_stats[item])
                    else:
                        copied_list.append(None)
                return copied_list
            #stats = [copyStats(self.fStats), copyStats(self.bStats)]
            #stats = [self.fStats, self.bStats]

            stats_eigen = self.stats_eigen
            computedEigen = {}
            eigen_reverse_lookup = {}
            updateOps = []
            # sync copied stats
            # with tf.control_dependencies(removeNone(stats[0]) +
            # removeNone(stats[1])):
            with tf.control_dependencies([]):
                for stats_var in stats_eigen:
                    if stats_var not in computedEigen:
                        eigens = tf.self_adjoint_eig(stats_var)
                        e = eigens[0]
                        Q = eigens[1]
                        if self._use_float64:
                            e = tf.cast(e, tf.float32)
                            Q = tf.cast(Q, tf.float32)
                        updateOps.append(e)
                        updateOps.append(Q)
                        computedEigen[stats_var] = {'e': e, 'Q': Q}
                        eigen_reverse_lookup[e] = stats_eigen[stats_var]['e']
                        eigen_reverse_lookup[Q] = stats_eigen[stats_var]['Q']

            self.eigen_reverse_lookup = eigen_reverse_lookup
            self.eigen_update_list = updateOps

        return updateOps