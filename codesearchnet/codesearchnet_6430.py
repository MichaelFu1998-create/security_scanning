def mutate_node(node, context):
    """
    :type context: Context
    """
    context.stack.append(node)
    try:
        if node.type in ('tfpdef', 'import_from', 'import_name'):
            return

        if node.start_pos[0] - 1 != context.current_line_index:
            context.current_line_index = node.start_pos[0] - 1
            context.index = 0  # indexes are unique per line, so start over here!

        if hasattr(node, 'children'):
            mutate_list_of_nodes(node, context=context)

            # this is just an optimization to stop early
            if context.number_of_performed_mutations and context.mutation_id != ALL:
                return

        mutation = mutations_by_type.get(node.type)

        if mutation is None:
            return

        for key, value in sorted(mutation.items()):
            old = getattr(node, key)
            if context.exclude_line():
                continue

            new = evaluate(
                value,
                context=context,
                node=node,
                value=getattr(node, 'value', None),
                children=getattr(node, 'children', None),
            )
            assert not callable(new)
            if new is not None and new != old:
                if context.should_mutate():
                    context.number_of_performed_mutations += 1
                    context.performed_mutation_ids.append(context.mutation_id_of_current_index)
                    setattr(node, key, new)
                context.index += 1

            # this is just an optimization to stop early
            if context.number_of_performed_mutations and context.mutation_id != ALL:
                return
    finally:
        context.stack.pop()