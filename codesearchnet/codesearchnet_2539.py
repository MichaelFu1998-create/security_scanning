def extract_packing_plan(self, topology):
    """
    Returns the representation of packing plan that will
    be returned from Tracker.
    """
    packingPlan = {
        "id": "",
        "container_plans": []
    }

    if not topology.packing_plan:
      return packingPlan

    container_plans = topology.packing_plan.container_plans

    containers = []
    for container_plan in container_plans:
      instances = []
      for instance_plan in container_plan.instance_plans:
        instance_resources = {"cpu": instance_plan.resource.cpu,
                              "ram": instance_plan.resource.ram,
                              "disk": instance_plan.resource.disk}
        instance = {"component_name" : instance_plan.component_name,
                    "task_id" : instance_plan.task_id,
                    "component_index": instance_plan.component_index,
                    "instance_resources": instance_resources}
        instances.append(instance)
      required_resource = {"cpu": container_plan.requiredResource.cpu,
                           "ram": container_plan.requiredResource.ram,
                           "disk": container_plan.requiredResource.disk}
      scheduled_resource = {}
      if container_plan.scheduledResource:
        scheduled_resource = {"cpu": container_plan.scheduledResource.cpu,
                              "ram": container_plan.scheduledResource.ram,
                              "disk": container_plan.scheduledResource.disk}
      container = {"id": container_plan.id,
                   "instances": instances,
                   "required_resources": required_resource,
                   "scheduled_resources": scheduled_resource}
      containers.append(container)

    packingPlan["id"] = topology.packing_plan.id
    packingPlan["container_plans"] = containers
    return json.dumps(packingPlan)