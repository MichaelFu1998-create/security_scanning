def _get_instance_plans(self, packing_plan, container_id):
    """
    For the given packing_plan, return the container plan with the given container_id. If protobufs
    supported maps, we could just get the plan by id, but it doesn't so we have a collection of
    containers to iterate over.
    """
    this_container_plan = None
    for container_plan in packing_plan.container_plans:
      if container_plan.id == container_id:
        this_container_plan = container_plan

    # When the executor runs in newly added container by `heron update`,
    # there is no plan for this container. In this situation,
    # return None to bypass instance processes.
    if this_container_plan is None:
      return None
    return this_container_plan.instance_plans