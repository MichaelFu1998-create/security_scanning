def make_network_graph(compact, expression_names, lookup_names):
  """
  Make a network graph, represented as of nodes and a set of edges.  
  The nodes are represented as tuples: (name: string, input_dim: Dim, label: string, output_dim: Dim, children: set[name], features: string)
#   The edges are represented as dict of children to sets of parents: (child: string) -> [(parent: string, features: string)] 
  """
  nodes = set()
#   edges = defaultdict(set) # parent -> (child, extra)
  
  var_name_dict = dict()
  if expression_names:
    for e in graphviz_items: # e: Expression
      if e in expression_names:
        var_name_dict[e.vindex] = expression_names[e]
  
  rnn_bldr_name = defaultdict(lambda: chr(len(rnn_bldr_name)+ord('A')))
  def vidx2str(vidx): return '%s%s' % ('N', vidx)

  for e in graphviz_items: # e: Expression
    vidx = e.vindex
    f_name = e.name
    args = e.args
    output_dim = e.dim
    input_dim = None # basically just RNNStates use this since everything else has input_dim==output_dim
    children = set()
    node_type = '2_regular'
    
    if f_name == 'vecInput':
      [_dim] = args
      arg_strs = []
    elif f_name == 'inputVector':
      [_v] = args
      arg_strs = []
    elif f_name == 'matInput':
      [_d1, _d2] = args
      arg_strs = []
    elif f_name == 'inputMatrix':
      [_v, _d] = args
      arg_strs = []
    elif f_name == 'parameters':
      [_dim] = args
      arg_strs = []
      if compact:
        if vidx in var_name_dict:
          f_name = var_name_dict[vidx]
      node_type = '1_param'
    elif f_name == 'lookup_parameters':
      [_dim] = args
      arg_strs = []
      if compact:
        if vidx in var_name_dict:
          f_name = var_name_dict[vidx]
      node_type = '1_param'
    elif f_name == 'lookup':
      [p, idx, update] = args
      [_dim] = p.args
      if vidx in var_name_dict:
        name = var_name_dict[vidx]
      else:
        name = None
      item_name = None
      if lookup_names and p in expression_names:
        param_name = expression_names[p]
        if param_name in lookup_names:
          item_name = '\\"%s\\"' % (lookup_names[param_name][idx],)
      if compact:
        if item_name is not None:
          f_name = item_name
        elif name is not None:
          f_name = '%s[%s]' % (name, idx)
        else:
          f_name = 'lookup(%s)' % (idx)
        arg_strs = []
      else:
        arg_strs = [var_name_dict.get(p.vindex, 'v%d' % (p.vindex))]
        if item_name is not None:
          arg_strs.append(item_name)
        vocab_size = _dim[0]
        arg_strs.extend(['%s' % (idx), '%s' % (vocab_size), 'update' if update else 'fixed'])
      #children.add(vidx2str(p.vindex))
      #node_type = '1_param'
    elif f_name == 'RNNState':
      [arg, input_dim, bldr_type, bldr_num, state_idx] = args # arg==input_e
      rnn_name = rnn_bldr_name[bldr_num]
      if bldr_type.endswith('Builder'):
        bldr_type[:-len('Builder')]
      f_name = '%s-%s-%s' % (bldr_type, rnn_name, state_idx)
      if not compact:
        i = arg.vindex
        s = var_name_dict.get(i, 'v%d' % (i))
        arg_strs = [s]
      else:
        arg_strs = []
      children.add(vidx2str(arg.vindex))
      node_type = '3_rnn_state'
    else:
      arg_strs = []
      for arg in args:
        if isinstance(arg, Expression):
          if not compact:
            i = arg.vindex
            s = var_name_dict.get(i, 'v%d' % (i))
            arg_strs.append(s)
          children.add(vidx2str(arg.vindex))
        elif isinstance(arg, float) and compact:
          s = re.sub('0+$', '', '%.3f' % (arg))
          if s == '0.':
            s = str(arg)
          arg_strs.append(s)
        else:
          arg_strs.append(str(arg))
        
#     f_name = { ,
#              }.get(f_name, f_name)
      
    if compact:
      f_name = { 'add': '+',
                 'sub': '-',
                 'mul': '*',
                 'div': '/',
                 'cadd': '+',
                 'cmul': '*',
                 'cdiv': '/',
                 'scalarsub': '-',
                 'concatenate': 'cat',
                 'esum': 'sum',
                 'emax': 'max',
                 'emin': 'min',
               }.get(f_name, f_name)
      if arg_strs:
        str_repr = '%s(%s)' % (f_name, ', '.join(arg_strs))
      else:
        str_repr = f_name
    elif f_name == 'add':
      [a,b] = arg_strs
      str_repr = '%s + %s' % (a,b)
    elif f_name == 'sub':
      [a,b] = arg_strs
      str_repr = '%s - %s' % (a,b)
    elif f_name == 'mul':
      [a,b] = arg_strs
      str_repr = '%s * %s' % (a,b)
    elif f_name == 'div':
      [a,b] = arg_strs
      str_repr = '%s / %s' % (a,b)
    elif f_name == 'neg':
      [a,] = arg_strs
      str_repr = '-%s' % (a)
    elif f_name == 'affine_transform':
      str_repr = arg_strs[0]
      for i in xrange(1, len(arg_strs), 2):
        str_repr += ' + %s*%s' % tuple(arg_strs[i:i+2])
    else:
      if arg_strs is not None:
        str_repr = '%s(%s)' % (f_name, ', '.join(arg_strs))
      else:
        str_repr = f_name
        
    name = vidx2str(vidx)
    var_name = '%s' % (var_name_dict.get(vidx, 'v%d' % (vidx))) if not compact else ''
#     if show_dims:
#       str_repr = '%s\\n%s' % (shape_str(e.dim), str_repr)
    label = str_repr
    if not compact:
      label = '%s = %s' % (var_name, label)
    features = ''
#     if output_dim.invalid():
#       features += " [color=red,style=filled,fillcolor=red]"
#     node_def_lines.append('  %s [label="%s%s"] %s;' % (vidx2str(vidx), label_prefix, str_repr, ''))
    expr_name = expression_names[e] if compact and expression_names and (e in expression_names) and (expression_names[e] != f_name) else None
    nodes.add(GVNode(name, input_dim, label, output_dim, frozenset(children), features, node_type, expr_name))

  return nodes