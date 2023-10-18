def repartition(self, num_partitions, repartition_function=None):
    """Return a new Streamlet containing all elements of the this streamlet but having
    num_partitions partitions. Note that this is different from num_partitions(n) in
    that new streamlet will be created by the repartition call.
    If repartiton_function is not None, it is used to decide which parititons
    (from 0 to num_partitions -1), it should route each element to.
    It could also return a list of partitions if it wants to send it to multiple
    partitions.
    """
    from heronpy.streamlet.impl.repartitionbolt import RepartitionStreamlet
    if repartition_function is None:
      repartition_function = lambda x: x
    repartition_streamlet = RepartitionStreamlet(num_partitions, repartition_function, self)
    self._add_child(repartition_streamlet)
    return repartition_streamlet