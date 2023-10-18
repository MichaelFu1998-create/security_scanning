def check_consistency(self):
        """
        Make sure that the required comps are included in the list of
        components supplied by the user. Also check that the parameters are
        consistent across the many components.
        """
        error = False
        regex = re.compile('([a-zA-Z_][a-zA-Z0-9_]*)')

        # there at least must be the full model, not necessarily partial updates
        if 'full' not in self.modelstr:
            raise ModelError(
                'Model must contain a `full` key describing '
                'the entire image formation'
            )

        # Check that the two model descriptors are consistent
        for name, eq in iteritems(self.modelstr):
            var = regex.findall(eq)
            for v in var:
                # remove the derivative signs if there (dP -> P)
                v = re.sub(r"^d", '', v)
                if v not in self.varmap:
                    log.error(
                        "Variable '%s' (eq. '%s': '%s') not found in category map %r" %
                        (v, name, eq, self.varmap)
                    )
                    error = True

        if error:
            raise ModelError('Inconsistent varmap and modelstr descriptions')