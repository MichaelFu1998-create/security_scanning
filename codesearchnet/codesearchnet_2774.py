def to_table(result):
  ''' normalize raw result to table '''
  max_count = 20
  table, count = [], 0
  for role, envs_topos in result.items():
    for env, topos in envs_topos.items():
      for topo in topos:
        count += 1
        if count > max_count:
          continue
        else:
          table.append([role, env, topo])
  header = ['role', 'env', 'topology']
  rest_count = 0 if count <= max_count else count - max_count
  return table, header, rest_count