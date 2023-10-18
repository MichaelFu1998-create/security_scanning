def remove_random_edge_until_has_leaves(self) -> None:
        """Remove random edges until there is at least one leaf node."""
        while True:
            leaves = set(self.iter_leaves())
            if leaves:
                return
            self.remove_random_edge()