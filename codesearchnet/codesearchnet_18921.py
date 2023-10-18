def block_resource_fitnesses(self, block: block.Block):
        """Returns a map of nodename to average fitness value for this block.
        Assumes that required resources have been checked on all nodes."""

        # Short-circuit! My algorithm is terrible, so it doesn't work well for the edge case where
        # the block has no requirements
        if not block.resources:
            return {n: 1 for n in self.config.nodes.keys()}

        node_fitnesses = {}

        for resource in block.resources:
            resource_fitnesses = self.resource_fitnesses(resource)

            if not resource_fitnesses:
                raise UnassignableBlock(block.name)

            max_fit = max(resource_fitnesses.values())
            min_fit = min(resource_fitnesses.values())

            for node, fitness in resource_fitnesses.items():
                if node not in node_fitnesses:
                    node_fitnesses[node] = {}

                if not fitness:
                    # Since we're rescaling, 0 is now an OK value...
                    # We will check for `is False` after this
                    node_fitnesses[node][resource.describe()] = False
                else:
                    if max_fit - min_fit:
                        node_fitnesses[node][resource.describe()] = (fitness - min_fit) / (max_fit - min_fit)
                    else:
                        # All the values are the same, default to 1
                        node_fitnesses[node][resource.describe()] = 1.0

        res = {}

        for node, res_fits in node_fitnesses.items():
            fit_sum = 0
            for res_desc, fit in res_fits.items():
                if fit is False:
                    fit_sum = False
                    break

                fit_sum += fit

            if fit_sum is False:
                # Skip this node entirely
                res[node] = False
                continue

            res[node] = fit_sum

        return res