def __find_block_center(self, level_blocks, unhandled_block_indexes):
        """!
        @brief Search block that is cluster center for new cluster.

        @return (bang_block) Central block for new cluster, if cluster is not found then None value is returned.

        """
        for i in reversed(range(len(level_blocks))):
            if level_blocks[i].get_density() <= self.__density_threshold:
                return None

            if level_blocks[i].get_cluster() is None:
                unhandled_block_indexes.remove(i)
                return level_blocks[i]

        return None