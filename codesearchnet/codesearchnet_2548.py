def to_table(components, topo_info):
  """ normalize raw logical plan info to table """
  inputs, outputs = defaultdict(list), defaultdict(list)
  for ctype, component in components.items():
    if ctype == 'bolts':
      for component_name, component_info in component.items():
        for input_stream in component_info['inputs']:
          input_name = input_stream['component_name']
          inputs[component_name].append(input_name)
          outputs[input_name].append(component_name)
  info = []
  spouts_instance = topo_info['physical_plan']['spouts']
  bolts_instance = topo_info['physical_plan']['bolts']
  for ctype, component in components.items():
    # stages is an int so keep going
    if ctype == "stages":
      continue
    for component_name, component_info in component.items():
      row = [ctype[:-1], component_name]
      if ctype == 'spouts':
        row.append(len(spouts_instance[component_name]))
      else:
        row.append(len(bolts_instance[component_name]))
      row.append(','.join(inputs.get(component_name, ['-'])))
      row.append(','.join(outputs.get(component_name, ['-'])))
      info.append(row)
  header = ['type', 'name', 'parallelism', 'input', 'output']
  return info, header