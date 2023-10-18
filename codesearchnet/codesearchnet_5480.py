def get_source_chains(self, blockade_id):
        """Get a map of blockade chains IDs -> list of IPs targeted at them

        For figuring out which container is in which partition
        """
        result = {}
        if not blockade_id:
            raise ValueError("invalid blockade_id")
        lines = self.get_chain_rules("FORWARD")

        for line in lines:
            parts = line.split()
            if len(parts) < 4:
                continue
            try:
                partition_index = parse_partition_index(blockade_id, parts[0])
            except ValueError:
                continue  # not a rule targetting a blockade chain

            source = parts[3]
            if source:
                result[source] = partition_index
        return result