def __process_by_ccore(self):
        """!
        @brief Performs cluster analysis using CCORE (C/C++ part of pyclustering library).

        """

        (self.__clusters, self.__noise, self.__ordering, self.__eps,
         objects_indexes, objects_core_distances, objects_reachability_distances) = \
            wrapper.optics(self.__sample_pointer, self.__eps, self.__minpts, self.__amount_clusters, self.__data_type)

        self.__optics_objects = []
        for i in range(len(objects_indexes)):
            if objects_core_distances[i] < 0.0:
                objects_core_distances[i] = None

            if objects_reachability_distances[i] < 0.0:
                objects_reachability_distances[i] = None

            optics_object = optics_descriptor(objects_indexes[i], objects_core_distances[i], objects_reachability_distances[i])
            optics_object.processed = True

            self.__optics_objects.append(optics_object)