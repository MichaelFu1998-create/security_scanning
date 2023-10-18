def run(command, *args):
  """ run command """
  # show all clusters
  if command == 'clusters':
    return clusters.run(command, *args)

  # show topologies
  elif command == 'topologies':
    return topologies.run(command, *args)

  # physical plan
  elif command == 'containers':
    return physicalplan.run_containers(command, *args)
  elif command == 'metrics':
    return physicalplan.run_metrics(command, *args)

  # logical plan
  elif command == 'components':
    return logicalplan.run_components(command, *args)
  elif command == 'spouts':
    return logicalplan.run_spouts(command, *args)
  elif command == 'bolts':
    return logicalplan.run_bolts(command, *args)

  # help
  elif command == 'help':
    return help.run(command, *args)

  # version
  elif command == 'version':
    return version.run(command, *args)

  return 1