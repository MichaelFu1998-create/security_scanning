def deserialize_task_spec(self, workflow, start_node, read_specs):
        """
        Reads the task from the given node and returns a tuple
        (start, end) that contains the stream of objects that model
        the behavior.

        workflow -- the workflow with which the task is associated
        start_node -- the xml structure (xml.dom.minidom.Node)
        """
        # Extract attributes from the node.
        nodetype = start_node.nodeName.lower()
        name = start_node.getAttribute('name').lower()
        context = start_node.getAttribute('context').lower()
        mutex = start_node.getAttribute('mutex').lower()
        cancel = start_node.getAttribute('cancel').lower()
        success = start_node.getAttribute('success').lower()
        times = start_node.getAttribute('times').lower()
        times_field = start_node.getAttribute('times-field').lower()
        threshold = start_node.getAttribute('threshold').lower()
        threshold_field = start_node.getAttribute('threshold-field').lower()
        file = start_node.getAttribute('file').lower()
        file_field = start_node.getAttribute('file-field').lower()
        kwargs = {'lock':        [],
                  'data':        {},
                  'defines':     {},
                  'pre_assign':  [],
                  'post_assign': []}
        if nodetype not in _spec_map:
            _exc('Invalid task type "%s"' % nodetype)
        if nodetype == 'start-task':
            name = 'start'
        if name == '':
            _exc('Invalid task name "%s"' % name)
        if name in read_specs:
            _exc('Duplicate task name "%s"' % name)
        if cancel != '' and cancel != '0':
            kwargs['cancel'] = True
        if success != '' and success != '0':
            kwargs['success'] = True
        if times != '':
            kwargs['times'] = int(times)
        if times_field != '':
            kwargs['times'] = operators.Attrib(times_field)
        if threshold != '':
            kwargs['threshold'] = int(threshold)
        if threshold_field != '':
            kwargs['threshold'] = operators.Attrib(threshold_field)
        if file != '':
            kwargs['file'] = file
        if file_field != '':
            kwargs['file'] = operators.Attrib(file_field)
        if nodetype == 'choose':
            kwargs['choice'] = []
        if nodetype == 'trigger':
            context = [context]
        if mutex != '':
            context = mutex

        # Walk through the children of the node.
        successors = []
        for node in start_node.childNodes:
            if node.nodeType != minidom.Node.ELEMENT_NODE:
                continue
            if node.nodeName == 'description':
                kwargs['description'] = node.firstChild.nodeValue
            elif node.nodeName == 'successor' \
                    or node.nodeName == 'default-successor':
                if node.firstChild is None:
                    _exc('Empty %s tag' % node.nodeName)
                successors.append((None, node.firstChild.nodeValue))
            elif node.nodeName == 'conditional-successor':
                successors.append(self.deserialize_condition(workflow, node))
            elif node.nodeName == 'define':
                key, value = self.deserialize_data(workflow, node)
                kwargs['defines'][key] = value
            # "property" tag exists for backward compatibility.
            elif node.nodeName == 'data' or node.nodeName == 'property':
                key, value = self.deserialize_data(workflow, node)
                kwargs['data'][key] = value
            elif node.nodeName == 'pre-assign':
                kwargs['pre_assign'].append(
                    self.deserialize_assign(workflow, node))
            elif node.nodeName == 'post-assign':
                kwargs['post_assign'].append(
                    self.deserialize_assign(workflow, node))
            elif node.nodeName == 'in':
                kwargs['in_assign'] = self.deserialize_assign_list(
                    workflow, node)
            elif node.nodeName == 'out':
                kwargs['out_assign'] = self.deserialize_assign_list(
                    workflow, node)
            elif node.nodeName == 'cancel':
                if node.firstChild is None:
                    _exc('Empty %s tag' % node.nodeName)
                if context == '':
                    context = []
                elif not isinstance(context, list):
                    context = [context]
                context.append(node.firstChild.nodeValue)
            elif node.nodeName == 'lock':
                if node.firstChild is None:
                    _exc('Empty %s tag' % node.nodeName)
                kwargs['lock'].append(node.firstChild.nodeValue)
            elif node.nodeName == 'pick':
                if node.firstChild is None:
                    _exc('Empty %s tag' % node.nodeName)
                kwargs['choice'].append(node.firstChild.nodeValue)
            else:
                _exc('Unknown node: %s' % node.nodeName)

        # Create a new instance of the task spec.
        module = _spec_map[nodetype]
        if nodetype == 'start-task':
            spec = module(workflow, **kwargs)
        elif nodetype == 'multi-instance' or nodetype == 'thread-split':
            if times == '' and times_field == '':
                _exc('Missing "times" or "times-field" in "%s"' % name)
            elif times != '' and times_field != '':
                _exc('Both, "times" and "times-field" in "%s"' % name)
            spec = module(workflow, name, **kwargs)
        elif context == '':
            spec = module(workflow, name, **kwargs)
        else:
            spec = module(workflow, name, context, **kwargs)

        read_specs[name] = spec, successors