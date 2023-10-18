def extract_physical_plan(self, topology):
    """
    Returns the representation of physical plan that will
    be returned from Tracker.
    """
    physicalPlan = {
        "instances": {},
        "instance_groups": {},
        "stmgrs": {},
        "spouts": {},
        "bolts": {},
        "config": {},
        "components": {}
    }

    if not topology.physical_plan:
      return physicalPlan

    spouts = topology.spouts()
    bolts = topology.bolts()
    stmgrs = None
    instances = None

    # Physical Plan
    stmgrs = list(topology.physical_plan.stmgrs)
    instances = list(topology.physical_plan.instances)

    # Configs
    if topology.physical_plan.topology.topology_config:
      physicalPlan["config"] = convert_pb_kvs(topology.physical_plan.topology.topology_config.kvs)

    for spout in spouts:
      spout_name = spout.comp.name
      physicalPlan["spouts"][spout_name] = []
      if spout_name not in physicalPlan["components"]:
        physicalPlan["components"][spout_name] = {
            "config": convert_pb_kvs(spout.comp.config.kvs)
        }
    for bolt in bolts:
      bolt_name = bolt.comp.name
      physicalPlan["bolts"][bolt_name] = []
      if bolt_name not in physicalPlan["components"]:
        physicalPlan["components"][bolt_name] = {
            "config": convert_pb_kvs(bolt.comp.config.kvs)
        }

    for stmgr in stmgrs:
      host = stmgr.host_name
      cwd = stmgr.cwd
      shell_port = stmgr.shell_port if stmgr.HasField("shell_port") else None
      physicalPlan["stmgrs"][stmgr.id] = {
          "id": stmgr.id,
          "host": host,
          "port": stmgr.data_port,
          "shell_port": shell_port,
          "cwd": cwd,
          "pid": stmgr.pid,
          "joburl": utils.make_shell_job_url(host, shell_port, cwd),
          "logfiles": utils.make_shell_logfiles_url(host, shell_port, cwd),
          "instance_ids": []
      }

    instance_groups = collections.OrderedDict()
    for instance in instances:
      instance_id = instance.instance_id
      stmgrId = instance.stmgr_id
      name = instance.info.component_name
      stmgrInfo = physicalPlan["stmgrs"][stmgrId]
      host = stmgrInfo["host"]
      cwd = stmgrInfo["cwd"]
      shell_port = stmgrInfo["shell_port"]


      # instance_id format container_<index>_component_1
      # group name is container_<index>
      group_name = instance_id.rsplit("_", 2)[0]
      igroup = instance_groups.get(group_name, list())
      igroup.append(instance_id)
      instance_groups[group_name] = igroup

      physicalPlan["instances"][instance_id] = {
          "id": instance_id,
          "name": name,
          "stmgrId": stmgrId,
          "logfile": utils.make_shell_logfiles_url(host, shell_port, cwd, instance.instance_id),
      }
      physicalPlan["stmgrs"][stmgrId]["instance_ids"].append(instance_id)
      if name in physicalPlan["spouts"]:
        physicalPlan["spouts"][name].append(instance_id)
      else:
        physicalPlan["bolts"][name].append(instance_id)

    physicalPlan["instance_groups"] = instance_groups

    return physicalPlan