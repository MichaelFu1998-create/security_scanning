def get_graphs_by_ids(self, network_ids: Iterable[int]) -> List[BELGraph]:
        """Get several graphs by their identifiers."""
        return [
            self.networks[network_id]
            for network_id in network_ids
        ]