def destroySynapse(self, synapse):
    """
    Destroys a synapse.

    :param synapse: (:class:`Synapse`) synapse to destroy
    """

    self._numSynapses -= 1

    self._removeSynapseFromPresynapticMap(synapse)

    synapse.segment._synapses.remove(synapse)