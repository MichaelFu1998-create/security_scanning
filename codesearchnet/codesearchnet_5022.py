def __process_by_python(self):
        """!
        @brief Performs cluster analysis using python code.

        """
        self.__create_queue()  # queue
        self.__create_kdtree()  # create k-d tree

        while len(self.__queue) > self.__number_cluster:
            cluster1 = self.__queue[0]  # cluster that has nearest neighbor.
            cluster2 = cluster1.closest  # closest cluster.

            self.__queue.remove(cluster1)
            self.__queue.remove(cluster2)

            self.__delete_represented_points(cluster1)
            self.__delete_represented_points(cluster2)

            merged_cluster = self.__merge_clusters(cluster1, cluster2)

            self.__insert_represented_points(merged_cluster)

            # Pointers to clusters that should be relocated is stored here.
            cluster_relocation_requests = []

            # Check for the last cluster
            if len(self.__queue) > 0:
                merged_cluster.closest = self.__queue[0]  # arbitrary cluster from queue
                merged_cluster.distance = self.__cluster_distance(merged_cluster, merged_cluster.closest)

                for item in self.__queue:
                    distance = self.__cluster_distance(merged_cluster, item)
                    # Check if distance between new cluster and current is the best than now.
                    if distance < merged_cluster.distance:
                        merged_cluster.closest = item
                        merged_cluster.distance = distance

                    # Check if current cluster has removed neighbor.
                    if (item.closest is cluster1) or (item.closest is cluster2):
                        # If previous distance was less then distance to new cluster then nearest cluster should
                        # be found in the tree.
                        if item.distance < distance:
                            (item.closest, item.distance) = self.__closest_cluster(item, distance)

                            # TODO: investigation is required. There is assumption that itself and merged cluster
                            # should be always in list of neighbors in line with specified radius. But merged cluster
                            # may not be in list due to error calculation, therefore it should be added manually.
                            if item.closest is None:
                                item.closest = merged_cluster
                                item.distance = distance

                        else:
                            item.closest = merged_cluster
                            item.distance = distance

                        cluster_relocation_requests.append(item)

            # New cluster and updated clusters should relocated in queue
            self.__insert_cluster(merged_cluster)
            for item in cluster_relocation_requests:
                self.__relocate_cluster(item)

        # Change cluster representation
        self.__clusters = [cure_cluster_unit.indexes for cure_cluster_unit in self.__queue]
        self.__representors = [cure_cluster_unit.rep for cure_cluster_unit in self.__queue]
        self.__means = [cure_cluster_unit.mean for cure_cluster_unit in self.__queue]