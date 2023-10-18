def get_type(self):
        """!
        @brief Returns algorithm type that corresponds to specified enumeration value.

        @return (type) Algorithm type for cluster analysis.

        """
        if self == silhouette_ksearch_type.KMEANS:
            return kmeans
        elif self == silhouette_ksearch_type.KMEDIANS:
            return kmedians
        elif self == silhouette_ksearch_type.KMEDOIDS:
            return kmedoids
        else:
            return None