def join(self, *groupnames):
        """Return an index group that contains atoms from all  *groupnames*.

        The method will silently ignore any groups that are not in the
        index.

        **Example**

        Always make a solvent group from water and ions, even if not
        all ions are present in all simulations::

           I['SOLVENT'] = I.join('SOL', 'NA+', 'K+', 'CL-')
        """
        return self._sum([self[k] for k in groupnames if k in self])